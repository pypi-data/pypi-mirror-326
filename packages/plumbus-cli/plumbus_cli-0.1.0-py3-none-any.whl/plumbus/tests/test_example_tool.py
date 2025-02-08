from tools.example_tool import run

def test_example_tool(capsys):
    run()
    captured = capsys.readouterr()
    assert "Running example tool!" in captured.out
