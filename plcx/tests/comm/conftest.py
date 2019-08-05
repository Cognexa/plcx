import socket
import pytest
import time
import threading


@pytest.fixture(scope='session')
def tcp_server():
    """Run testing tcp server."""
    host, port = 'localhost', 33888

    def server():
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soc:
            soc.bind((host, port))
            soc.listen(1)

            while True:
                try:
                    conn, addr = soc.accept()
                    while True:
                        message = conn.recv(512)  # read just 512 bytes
                        if not message:
                            break
                        time.sleep(0.05)  # wait to response
                        conn.sendall(f'received:{message.decode()!r}'.encode())
                    conn.close()
                except ConnectionResetError:
                    pass

    thread = threading.Thread(target=server, name='server')
    thread.daemon = True
    thread.start()
    yield host, port


@pytest.fixture
def tcp_client():
    """Return function to send message to server."""
    host, port = 'localhost', 33889

    def client(message: bytes, read_bytes: int = 0) -> bytes:
        """
        Send message to server.

        :param message: message to send
        :param read_bytes: size of bytes read as response
        :return: bytes response
        """
        try_count = 0
        while try_count < 3:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soc:
                # try to make connection
                try:
                    soc.connect((host, port))  # connect to server
                except:
                    time.sleep(.1)
                    try_count += 1
                    continue

                soc.send(message)  # send message
                response = soc.recv(read_bytes)  # receive response to message
                soc.close()  # close server
            return response

    yield host, port, client
