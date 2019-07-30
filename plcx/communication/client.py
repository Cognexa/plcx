import asyncio

from typing import Any, Optional


async def tcp_echo_client(
        message: bytes,
        host: str,
        port: int,
        response_size: Optional[int] = None
) -> Optional[bytes]:
    """
    Send message to server.

    :param message: bytes message
    :param host: host url or ip
    :param port: host port
    :param response_size: bytes size of response, if None not wait for any response [None]
    :return: response bytes message or None
    """
    response = None
    # open connection
    reader, writer = await asyncio.open_connection(host=host, port=port)
    # send message to server
    writer.write(message)
    # get response
    if response_size:
        response = await reader.read(response_size)
    # close connection
    writer.close()

    return response


class Client:
    def __init__(self, host: str, port: int):
        self._host = host
        self._port = port

    def send(self, message: bytes, response_size: Optional[int] = None) -> Any:
        """
        Send message.

        :param message: bytes massage
        :param response_size: bytes size of response, if None not wait for any response [None]
        :return: response bytes message or None
        """
        return tcp_echo_client(message, self._host, self._port, response_size)
