import asyncio
import forge
import logging
import threading

from contextlib import contextmanager
from typing import Callable

logger = logging.getLogger(__name__)


def tcp_read_echo(response_handler: Callable, read_bytes: int = 512, time_out: int = 1) -> asyncio.coroutine:
    """
    Read and response to the message from the client.

    :param response_handler: function to handler message and make response
    :param read_bytes: number of reading bytes
    :param time_out: waiting time out, use in connection and reading response [1 second]
    :return: coroutine handler
    """
    if not callable(response_handler):
        raise AttributeError('response_handler must be callable function')

    async def echo_handler(reader, writer) -> None:
        """
        Receive message from client.

        :param reader: client reader
        :param writer: client writer
        :return:
        """
        # read message
        message = await asyncio.wait_for(reader.read(read_bytes), timeout=time_out)  # max number of bytes to read

        # wait for message response
        response = b''
        try:
            response = response_handler(message)
        except Exception as error:
            response = f'{error.__class__.__name__}'.encode()
        finally:
            # send response
            writer.write(response)

            # close writer
            await writer.drain()
            writer.close()

    return echo_handler


def serverx(
        host: str,
        port: int,
        response_handler: Callable,
        read_bytes: int = 512,
        time_out: int = 1
) -> asyncio.AbstractEventLoop:
    """
    Initialized event loop and add server to it.

    :param host: server host name or ip
    :param port: server port
    :param response_handler: function to handler message and make response
    :param read_bytes: number of reading bytes
    :param time_out: waiting time out, use in connection and reading response [1 second]
    :return: asyncio event loop
    """
    loop = asyncio.new_event_loop()
    server = asyncio.start_server(tcp_read_echo(response_handler, read_bytes, time_out), host, port, loop=loop)
    loop.create_task(server)

    return loop


@forge.copy(serverx)
@contextmanager
def serverx_in_thread(*args, **kwargs) -> threading.Thread:
    """
    Run Server in thread.

    :return: server thread
    """

    loop = serverx(*args, **kwargs)
    thread = threading.Thread(target=loop.run_forever, name='server')
    thread.start()
    logger.info(f'Thread `({thread.ident}, {thread.name})` was start.')
    try:
        yield thread
    finally:
        loop.call_soon_threadsafe(loop.stop)
        thread.join()
        loop.close()
        logger.info(f'Thread `({thread.ident}, {thread.name})` was stopped.')
