#!/usr/bin/env python3
import sys
import requests
import pika
import typer
import re
from rich.progress import Progress
from typing_extensions import Annotated


def resolve_management_url_and_auth(amqp_url):
    pattern = r"^amqps:\/\/(?P<username>[^:]+):(?P<password>[^@]+)@(?P<host>[^:\/]+):(?P<port>\d+)(\/.*)?$"
    match = re.match(pattern, amqp_url)
    if not match:
        raise ValueError(f"Invalid AMQP URL format: {amqp_url}")

    username = match.group("username")
    password = match.group("password")
    host = match.group("host")
    
    mgmt_url = f"https://{host}:443"
    return mgmt_url, (username, password)

def list_queues(amqp_url, vhost):
    mgmt_url, auth = resolve_management_url_and_auth(amqp_url)

    url = f"{mgmt_url}/api/queues{vhost}"
    try:
        response = requests.get(url, auth=auth)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error retrieving queues from source: {e}")
        raise typer.Exit(1)
    return response.json()

def get_source_queues(source_mgmt_url, source_auth, vhost_encoded):
    url = f"{source_mgmt_url}/api/queues/{vhost_encoded}"
    try:
        response = requests.get(url, auth=source_auth)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error retrieving queues from source: {e}")
        sys.exit(1)
    return response.json()

def process_queue(queue_name, queue_message_count, source_channel, dest_channel):
    transferred = 0
    print(f"Processing queue '{queue_name}'...")

    with Progress() as progress:

        transfer = progress.add_task("Transferring Messages...", total=queue_message_count)

        while True:
            method_frame, properties, body = source_channel.basic_get(queue=queue_name, auto_ack=False)
            if method_frame is None:
                break
            else:
                dest_channel.basic_publish(
                    exchange='',
                    routing_key=queue_name,
                    body=body,
                    properties=properties
                )
                source_channel.basic_ack(delivery_tag=method_frame.delivery_tag)
                # print(f"  Transferred message (delivery_tag={method_frame.delivery_tag}).")
                progress.update(transfer, advance=1)
                transferred += 1
    print(f"Finished processing queue '{queue_name}'. Transferred {transferred} messages.\n")
    
def run(
        source_amqp_url, 
        dest_amqp_url, 
        queue: Annotated[str, typer.Option(help="Name of the specific queue to process for testing. If omitted, all queues (with messages) from the source will be processed.")] = None,
        vhost: Annotated[str, typer.Option(help="RabbitMQ vhost to use")] = "/",
        dry_run: Annotated[bool, typer.Option(help="Don't make any changes, only simulate")] = False,
    ):
    """
    Mass transfer messages from RabbitMQ source to destination using AMQP. \n
    
    Useful for unidirectional one-time data migration between RabbitMQ brokers.\n
    1. Retrieves all queues from the source RabbitMQ broker.\n
    2. For each non-empty queue, checks if the destination broker has a matching queue.\n
    3. If the destination queue exists, transfers messages from the source to the destination.\n  
    """

    if dry_run:
        print("Running in DRY RUN mode. No messages will actually be transferred.")
    
    print("Retrieving queues from source broker...")
    source_queues = list_queues(source_amqp_url, vhost)
    if not source_queues:
        print("No queues found on the source broker.")
        raise typer.Exit(1)
    
    print("Retrieving queues from destination broker...")
    dest_queues = list_queues(dest_amqp_url, vhost)
    if not dest_queues:
        print("No queues found on the source broker.")
        raise typer.Exit(1)

    if queue:
        if not any(q["name"] == queue for q in source_queues):
            print(f"Queue '{queue}' not found on the source broker. Exiting.")
            raise typer.Exit(1)
        if not any(q["name"] == queue for q in dest_queues):
            print(f"Queue '{queue}' not found on the destination broker. Exiting.")
            raise typer.Exit(1)
        
        source_queues = [q for q in source_queues if q["name"] == queue]
        print(f"Only processing queue '{queue}'.")

    print("Connecting to source and destination brokers...")
    try:
        source_params = pika.URLParameters(source_amqp_url)
        source_connection = pika.BlockingConnection(source_params)
        source_channel = source_connection.channel()
    except Exception as e:
        print(f"Error connecting to source broker via AMQP: {e}")
        raise typer.Exit(1)
    
    try:
        dest_params = pika.URLParameters(dest_amqp_url)
        dest_connection = pika.BlockingConnection(dest_params)
        dest_channel = dest_connection.channel()
    except Exception as e:
        print(f"Error connecting to destination broker via AMQP: {e}")
        raise typer.Exit(1)
    
    print("Processing queues...")
    for q in source_queues:
        queue_name = q["name"]
        message_count = q.get("messages", 0)
        if queue:
            print(f"Queue '{queue_name}' (message count: {message_count}).")
        else:
            if message_count <= 0:
                print(f"Skipping queue '{queue_name}' because it has no messages.")
                continue
            print(f"\nQueue '{queue_name}' has {message_count} messages:")

        if not any(q["name"] == queue_name for q in dest_queues):
            print(f"  [!] Destination queue '{queue_name}' does not exist. Skipping message transfer for this queue.")
            continue
        else:
            print(f"  [i] Destination queue '{queue_name}' exists.")
        
        if dry_run:
            print(f"DRY RUN: Would transfer messages from queue '{queue_name}'.\n")
        else:
            process_queue(queue_name, message_count, source_channel, dest_channel)
    
    source_connection.close()
    dest_connection.close()
