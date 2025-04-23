from typer import Typer
from server import start_server

app = Typer()

@app.command()
def start(port: int, origin: str):
    start_server(port, origin)

if __name__ == '__main__':
    app()