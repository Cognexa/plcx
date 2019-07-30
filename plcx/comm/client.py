import asyncio

from typing import Optional


async def tcp_send_echo(
        message: bytes,
        host: str,
        port: int,
        loop: Optional[asyncio.AbstractEventLoop] = None,
        response_bytes: int = 0

) -> bytes:
    """
    Send message to server.

    :param message: bytes message
    :param host: host url or ip
    :param port: host port
    :param loop: asyncio event loop
    :param response_bytes: max number of bytes to read [0 == empty response]
    :return:
    """
    # open connection
    reader, writer = await asyncio.open_connection(host=host, port=port, loop=loop)
    # send message to server
    writer.write(message)
    # get response
    response = await reader.read(response_bytes)
    # close connection
    writer.close()
    return response


class Client:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.loop = asyncio.new_event_loop()

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.loop.close()

    def send(self, message: bytes, response_bytes: int = 0) -> bytes:
        """
        Send message.

        :param message: bytes massage
        :param response_bytes: max number of bytes to read [0 == empty response]
        :return: response bytes message or None
        """
        return self.loop.run_until_complete(
            tcp_send_echo(message, self.host, self.port, self.loop, response_bytes)
        )
