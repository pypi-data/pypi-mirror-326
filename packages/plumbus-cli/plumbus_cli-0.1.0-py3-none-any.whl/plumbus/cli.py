import typer
from .tools import rabbitmq_shovel
from rich import print

app = typer.Typer(no_args_is_help=True)

rabbitmq_app = typer.Typer(no_args_is_help=True)
rabbitmq_app.command("shovel", no_args_is_help=True)(rabbitmq_shovel.run)

app.add_typer(rabbitmq_app, name="rabbitmq", help="RabbitMQ related tools",)

@app.command()
def hello():
    """
    Print a friendly greeting.
    """
    print("Hello, World! Everybody needs a plumbus in their home :)")
    raise typer.Exit()

if __name__ == "__main__":
    app()
