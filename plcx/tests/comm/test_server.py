import pytest

from plcx.comm.server import serverx_in_thread


def test_server_context(tcp_client):
    """
    Test serverx object for reading message form client.

    :param tcp_client: function for send message to server
    """
    host, port, client = tcp_client
    with serverx_in_thread(host, port, lambda x: b'ok', 16) as thread:

        assert thread.name == 'server'
        assert thread.is_alive()

        assert client(b'test', 4) == b'ok'
        assert client(b'test', 4) == b'ok'

    assert not thread.is_alive()


def test_server_context_error(tcp_client):
    """
    Test raising error of serverx.

    :param tcp_client: function for send message to server
    """
    host, port, client = tcp_client

    # add not callable object as message handler
    with pytest.raises(AttributeError):
        with serverx_in_thread(host, port, None, 16):
            pass

    # massage handler raise error
    def raise_handler(*args, **kwargs):
        raise TimeoutError('time out')

    with serverx_in_thread(host, port, response_handler=raise_handler):
        assert client(b'test', 32) == b'TimeoutError'

    # massage handler without arguments
    def not_arg_handler():
        pass

    with serverx_in_thread(host, port, response_handler=not_arg_handler):
        assert client(b'test', 9) == b'TypeError'
