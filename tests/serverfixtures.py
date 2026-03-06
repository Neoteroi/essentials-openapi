import socket
from multiprocessing import Process
from time import sleep

import pytest
from flask import Flask

SERVER_PORT = 44777
BASE_URL = f"http://127.0.0.1:{SERVER_PORT}"


app = Flask(__name__, static_url_path="", static_folder="res")


def start_server():
    app.run(host="127.0.0.1", port=44777)


def _wait_for_server(host, port, timeout=10.0):
    import time

    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        try:
            with socket.create_connection((host, port), timeout=0.1):
                return
        except OSError:
            time.sleep(0.05)
    raise RuntimeError(f"Server on {host}:{port} did not start within {timeout}s")


def _start_server_process(target):
    server_process = Process(target=target)
    server_process.start()
    _wait_for_server("127.0.0.1", SERVER_PORT)

    if not server_process.is_alive():
        raise TypeError("The server process did not start!")

    yield 1

    sleep(1.2)
    server_process.terminate()


@pytest.fixture(scope="module", autouse=True)
def test_server():
    yield from _start_server_process(start_server)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=44778, debug=True)
