import asyncio
import logging

from typing import Callable

logger = logging.getLogger(__name__)


def tcp_read_echo(response_handler: Callable, read_bytes: int = 512, time_out: float = 1) -> asyncio.coroutine:
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
            response = error.__class__.__name__.encode()
        finally:
            # send response
            writer.write(response)

            # close writer
            await writer.drain()
            writer.close()

    return echo_handler


async def serverx(
        host: str,
        port: int,
        response_handler: Callable,
        read_bytes: int = 512,
        time_out: float = 1,
        max_try: int = 3
) -> asyncio.AbstractServer:
    """
    Initialized event loop and add server to it.

    :param host: server host name or ip
    :param port: server port
    :param response_handler: function to handler message and make response
    :param read_bytes: number of reading bytes
    :param time_out: waiting time out, use in connection and reading response [1 second]
    :param max_try: maximum attention to create server
    :return: asyncio abstract server
    """
    try_count = 0
    while True:
        try:
            return await asyncio.start_server(tcp_read_echo(response_handler, read_bytes, time_out), host, port)
        except OSError as error:
            try_count += 1
            if try_count >= max_try:
                raise error

            await asyncio.sleep(0.2)  # wait for new try
            continue
