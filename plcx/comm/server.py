import asyncio
import logging

from typing import Callable

from plcx.constants import MAX_TRY
from plcx.exceptions import NotReadableMessage

logger = logging.getLogger(__name__)


def tcp_read_echo(response_handler: Callable, read_bytes: int = 512) -> asyncio.coroutine:
    """
    Read and response to the message from the client.

    :param response_handler: function to handler message and make response
    :param read_bytes: number of reading bytes
    :return: coroutine handler
    """
    if not callable(response_handler):
        raise AttributeError('response_handler must be callable function')

    async def echo_handler(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        """
        Receive message from client.

        :param reader: client reader
        :param writer: client writer
        :return:
        """
        while not writer.is_closing():
            try:
                # read message
                message = await reader.read(read_bytes)  # max number of bytes to read

                # wait for message response
                response_handler(message, reader, writer)

                # flush the write buffer
                await writer.drain()

            except NotReadableMessage as error:
                # do not close connection if this error type
                logger.warning(error)

            except Exception as error:
                logger.error(error)
                raise error

        writer.close()

    return echo_handler


async def serverx(
        host: str,
        port: int,
        response_handler: Callable,
        read_bytes: int = 512,
        max_try: int = MAX_TRY,
) -> asyncio.AbstractServer:
    """
    Initialized event loop and add server to it.

    :param host: server host name or ip
    :param port: server port
    :param response_handler: function to handler message and make response
    :param read_bytes: number of reading bytes
    :param max_try: maximum attention to create server
    :return: asyncio abstract server
    """
    try_count = 0
    while True:
        try:
            return await asyncio.start_server(tcp_read_echo(response_handler, read_bytes), host, port)
        except (OSError, asyncio.TimeoutError) as error:
            try_count += 1
            if try_count >= max_try:
                raise error

            await asyncio.sleep(0.5)  # wait for new try
