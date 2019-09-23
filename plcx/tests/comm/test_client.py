import asyncio

import pytest
from plcx.comm.client import ClientX, clientx


@pytest.mark.parametrize("msg", ["1", "123", "hola"])
def test_clientx(tcp_server, msg):
    """
    Test tcp clientx coroutine.

    :param tcp_server: tuple with host and port of testing server
    :param msg: message to send
    """
    host, port = tcp_server
    loop = asyncio.get_event_loop()

    assert loop.run_until_complete(clientx(host, port, msg.encode(), 32, time_out=5)).decode() == f"received:'{msg}'"
    assert (
        loop.run_until_complete(clientx(host, port, b"control message", 32, time_out=5))
        == b"received:'control message'"
    )


@pytest.mark.parametrize("msg", ["111", "321", "hi"])
def test_clientx_context(tcp_server, msg):
    """
    Test tcp clientx as context for connection to server.

    :param tcp_server: tuple with host and port of testing server
    :param msg: message to send
    """
    host, port = tcp_server
    client = ClientX(host=host, port=port)
    assert client.send(msg.encode(), 32, time_out=5).decode() == f"received:'{msg}'"
    assert client.send(b"control message", 32, time_out=5) == b"received:'control message'"


def test_clientx_error(tcp_server):
    """
    Test raising error.

    :param tcp_server: tuple with host and port of testing server
    """
    host, port = tcp_server

    loop = asyncio.get_event_loop()

    # testing connection to port 0
    with pytest.raises((OSError, asyncio.TimeoutError)):
        loop.run_until_complete(clientx(host, 0, b"", 1, max_try=1))

    # testing connection to not exist port
    with pytest.raises((OSError, asyncio.TimeoutError)):
        loop.run_until_complete(clientx(host, 65432, b"", 1, max_try=1))

    # testing connection to not exist address
    with pytest.raises((OSError, asyncio.TimeoutError)):
        loop.run_until_complete(clientx("hola", port, b"", 1, max_try=1))

    # testing time out
    with pytest.raises((OSError, asyncio.TimeoutError)):
        loop.run_until_complete(clientx(host, port, b"123", 16, time_out=0.005, max_try=1))
