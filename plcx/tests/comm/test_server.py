import asyncio
import logging
import pytest
import time
import threading

from plcx.comm.server import serverx


class StoppableServerThread(threading.Thread):
    """
    Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition.
    """

    def __init__(self, host, port, echo_handler, max_try=10):
        super(StoppableServerThread, self).__init__()
        self._stop_event = threading.Event()
        self.host = host
        self.port = port
        self.max_try = max_try
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
        server_ = loop.create_task(
            serverx(self.host, self.port, self.echo_handler, 16, max_try=self.max_try)
        )
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

    def handler(message, reader, writer):
        logging.info(f'got message: `{message}`')
        logging.debug(f'got reader: `{reader}` and `{writer}`')
        writer.write(b'ok')

    thread = StoppableServerThread(host, port, handler)
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
    time.sleep(0.3)  # wait while serve is starting

    with pytest.raises(OSError):
        asyncio.run(serverx(host, port, lambda x: b'ok', 16, max_try=1))

    thread.stop()
    thread.join()


def raise_timeout(*args, **kwargs):
    raise TimeoutError(f'timeout error with args: `{args}` and kwargs: `{kwargs}`')


def raise_handler(*args, **kwargs):
    raise AttributeError(f'attribute error with args: `{args}` and kwargs: `{kwargs}`')


def not_arg_handler():
    pass


@pytest.mark.parametrize("handler, exp_error", [
    (raise_timeout, TimeoutError),
    (raise_handler, AttributeError),
    (not_arg_handler, TypeError)
])
def test_serverx_error(tcp_client, caplog, handler, exp_error):
    """
    Test raising error of serverx.

    :param tcp_client: function for send message to server
    :param caplog: capture logs
    :param handler: echo handler
    :param exp_error: expected error
    """
    host, port, client = tcp_client

    thread = StoppableServerThread(host, port, handler, max_try=1)
    thread.start()
    time.sleep(0.3)  # wait while serve is starting

    with caplog.at_level(logging.ERROR, logger="plcx.comm.server"):
        assert client(b'test', 4) is None

        assert all([record.name == "plcx.comm.server" for record in caplog.records if record.filename == 'server.py'])
        assert all(
            [
                issubclass(record.exc_info[0], exp_error)
                for record in caplog.records if record.filename == 'base_events.py'
            ]
        )

    thread.stop()
    thread.join()
