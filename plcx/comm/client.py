import asyncio

from typing import Optional


async def tcp_send_echo(
        message: bytes,
        host: str,
        port: int,
        loop: Optional[asyncio.AbstractEventLoop] = None,
        response_bytes: int = 0,
        time_out: float = 1

) -> bytes:
    """
    Send message to server.

    :param message: bytes message
    :param host: host url or ip
    :param port: host port
    :param loop: asyncio event loop
    :param response_bytes: max number of bytes to read [0 == empty response]
    :param time_out: waiting time out, use in connection and reading response [1 second]
    :return:
    """
    # open connection with timeout
    reader, writer = await asyncio.wait_for(asyncio.open_connection(host=host, port=port, loop=loop), timeout=time_out)
    # send message to server
    writer.write(message)
    # get response with timeout
    response = await asyncio.wait_for(reader.read(response_bytes), timeout=time_out)
    # close connection
    writer.close()
    return response


class Client:
    def __init__(self, host: str, port: int):
        """
        Initialized client.

        :param host: server host name or ip
        :param port: server port
        """
        self.host = host
        self.port = port
        self.loop = asyncio.new_event_loop()

    def __del__(self):
        self.loop.stop()
        self.loop.close()
        del self

    def __enter__(self):
        if not self.loop.is_running():
            self.loop = asyncio.new_event_loop()
        return self

    def __exit__(self, *exc):
        self.loop.stop()
        self.loop.close()

    def send(self, message: bytes, response_bytes: int = 0, time_out: float = 1) -> bytes:
        """
        Send message.

        :param message: bytes massage
        :param response_bytes: max number of bytes to read [0 == empty response]
        :param time_out: waiting time out, use in connection and reading response
        :return: response bytes message or None
        """
        return self.loop.run_until_complete(
            tcp_send_echo(message, self.host, self.port, self.loop, response_bytes, time_out)
        )
