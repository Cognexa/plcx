import asyncio
import pytest
import time
import threading

from plcx.comm.server import serverx


class StoppableServerThread(threading.Thread):
    """
    Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition.
    """

    def __init__(self, host, port, echo_handler):
        super(StoppableServerThread, self).__init__()
        self._stop_event = threading.Event()
        self.host = host
        self.port = port
        self.echo_handler = echo_handler

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def run(self) -> None:
        async def killer(thread, server):
            while not thread.stopped():
                await asyncio.sleep(0.05)

            server.cancel()

        # define loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        # define tasks
        server_ = loop.create_task(serverx(self.host, self.port, self.echo_handler, 16, time_out=0.05, max_try=5))
        killer_ = loop.create_task(killer(self, server_))

        # run tasks
        try:
            _, srv = loop.run_until_complete(asyncio.gather(killer_, server_))
            srv.close()
            loop.run_until_complete(srv.wait_closed())
        finally:
            # clean up
            loop.stop()
            loop.close()


def test_serverx(tcp_client):
    """
    Test serverx object for reading message form client.

    :param tcp_client: function for send message to server
    """
    host, port, client = tcp_client

    thread = StoppableServerThread(host, port, lambda x: b'ok')
    thread.start()

    assert thread.is_alive()

    assert client(b'test', 4) == b'ok'
    assert client(b'test', 4) == b'ok'

    thread.stop()
    thread.join()

    assert not thread.is_alive()
    assert thread.stopped()


def test_serverx_try_connect(tcp_client):
    """
    Test server try make connection.

    :param tcp_client: function for send message to server
    """
    host, port, client = tcp_client

    thread = StoppableServerThread(host, port, lambda x: b'ok')
    thread.start()
    time.sleep(0.2)  # wait while serve is starting

    with pytest.raises(OSError):
        asyncio.run(serverx(host, port, lambda x: b'ok', 16, time_out=.2, max_try=1))

    thread.stop()
    thread.join()


def raise_handler(*args, **kwargs):
    raise TimeoutError(f'time out with args: `{args}` and kwargs: `{kwargs}`')


def not_arg_handler():
    pass


@pytest.mark.parametrize("handler, exp_message", [
    (raise_handler, b'TimeoutError'),
    (not_arg_handler, b'TypeError')
])
def test_serverx_error(tcp_client, handler, exp_message):
    """
    Test raising error of serverx.

    :param tcp_client: function for send message to server
    :param handler: echo handler
    :param exp_message: expected message form server
    """
    host, port, client = tcp_client

    thread = StoppableServerThread(host, port, handler)
    thread.start()

    assert client(b'test', 32) == exp_message

    thread.stop()
    thread.join()
