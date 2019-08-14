import asyncio
import logging

from dataclasses import dataclass
from typing import Tuple

logger = logging.getLogger(__name__)


async def connect(
        host: str,
        port: int,
        time_out: float = .5,
        max_try: int = 3,
) -> Tuple[asyncio.streams.StreamReader, asyncio.streams.StreamWriter]:
    """
    Create connection to server.

    :param host: host url or ip
    :param port: host port
    :param time_out: waiting time out, use in connection and reading response [.5 second]
    :param max_try: maximum attention to create server [3 times]
    :return:
    """
    try_count = 0
    while True:
        try:
            return await asyncio.wait_for(asyncio.open_connection(host=host, port=port), timeout=time_out)
        except OSError as error:
            try_count += 1
            if try_count >= max_try:
                raise error

            await asyncio.sleep(0.2)  # wait for new try
            continue


async def clientx(
        host: str,
        port: int,
        message: bytes,
        response_bytes: int = 0,
        time_out: float = .5,
        max_try: int = 3,

) -> bytes:
    """
    Send message to server.

    :param host: host url or ip
    :param port: host port
    :param message: bytes message
    :param response_bytes: max number of bytes to read [0 == empty response]
    :param time_out: waiting time out, use in connection and reading response [.5 second]
    :param max_try: maximum attention to create server [3 times]
    :return:
    """
    # open connection with timeout
    reader, writer = await connect(host, port, time_out, max_try)

    # send message to server
    writer.write(message)

    # get response with timeout
    response = await asyncio.wait_for(reader.read(response_bytes), timeout=time_out)

    # close connection
    writer.close()

    return response


@dataclass
class ClientX:
    host: str
    port: int

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        return True

    def send(self, message: bytes, response_bytes: int = 0, time_out: float = .5) -> bytes:
        """
        Send message.

        :param message: bytes massage
        :param response_bytes: max number of bytes to read [0 == empty response]
        :param time_out: waiting time out, use in connection and reading response
        :return: response bytes message or None
        """
        logger.debug(f'try send message with client to `{self.host}:{self.port}`')

        loop = asyncio.get_event_loop()
        return loop.run_until_complete(clientx(self.host, self.port, message, response_bytes, time_out))
