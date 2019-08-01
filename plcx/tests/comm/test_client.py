import asyncio
import pytest

from plcx.comm.client import clientx


@pytest.mark.parametrize('msg', ['1', '123', 'hola'])
def test_client_context(tcp_server, msg):
    """
    Test tcp client object for connection to server.

    :param tcp_server: tuple with host and port of testing server
    :param msg: message to send
    """
    host, port = tcp_server
    with clientx(host=host, port=port) as client:
        assert client.send(msg.encode(), 512).decode() == f"received:'{msg}'"
        assert client.send(b'control message', 512).decode() == "received:'control message'"


def test_client_context_new(tcp_server):
    """
    Test enter Client more time.

    :param tcp_server: tuple with host and port of testing server
    """
    host, port = tcp_server

    client = clientx(host=host, port=port)

    with client:
        response = client.send(b'123', 32)
        assert response.decode() == "received:'123'"

    assert client.loop.is_running() is False and client.loop.is_closed() is True

    # try create new client
    with client:
        response = client.send(b'123', 32)
        assert response.decode() == "received:'123'"



def test_client_context_error(tcp_server):
    """
    Test raising error.

    :param tcp_server: tuple with host and port of testing server
    """
    host, port = tcp_server

    # testing connection to port 0
    with pytest.raises(OSError):
        with clientx(host=host, port=0) as client:
            client.send(b'', 1)

    # testing connection to not exist port
    with pytest.raises(OSError):
        with clientx(host=host, port=65432) as client:
            client.send(b'', 1)

    # testing connection to not exist address
    with pytest.raises(OSError):
        with clientx(host='hola', port=port) as client:
            client.send(b'', 1)

    # testing time out
    with pytest.raises(asyncio.TimeoutError):
        with clientx(host=host, port=port) as client:
            client.send(b'123', 16, .005)

    # testing stopped loop
    with pytest.raises(RuntimeError):
        with clientx(host=host, port=port) as client:
            client.loop.stop()  # stop loop
            client.send(b'123')
