import asyncio
import pytest

from plcx.comm.client import Client


@pytest.mark.parametrize('msg', ['1', '123', 'hola'])
def test_client_context(tcp_server, msg):
    """
    Test tcp client object for connection to server.

    :param tcp_server: tuple with host and port of testing server
    :param msg: message to send
    """
    host, port = tcp_server
    with Client(host=host, port=port) as client:
        result = client.send(msg.encode(), 512)

    assert result.decode() == f"received:'{msg}'"


def test_client_context_error(tcp_server):
    """
    Test raising error.

    :param tcp_server: tuple with host and port of testing server
    """
    host, port = tcp_server

    # testing connection to port 0
    with pytest.raises(OSError):
        with Client(host=host, port=0) as client:
            client.send(b'', 1)

    # testing connection to not exist port
    with pytest.raises(OSError):
        with Client(host=host, port=65432) as client:
            client.send(b'', 1)

    # testing connection to not exist address
    with pytest.raises(OSError):
        with Client(host='hola', port=port) as client:
            client.send(b'', 1)

    # testing time out
    with pytest.raises(asyncio.TimeoutError):
        with Client(host=host, port=port) as client:
            client.send(b'123', 16, .05)
