import asyncio
import threading


def tcp_read_echo(read_bytes: int = 512) -> asyncio.coroutine:
    """
    Read message from client.

    :param read_bytes: number of reading bytes
    :return: coroutine handler
    """
    async def echo_handler(reader, writer) -> None:
        """
        Receive message from client.

        :param reader: client reader
        :param writer: client writer
        :return:
        """
        # read message
        message = await reader.read(read_bytes)  # max number of bytes to read

        # wait for message response
        # todo: use queue to get message response
        response = b'ok'

        # send response
        writer.write(response)

        await writer.drain()
        writer.close()

    return echo_handler


def serverx(host: str, port: int, read_bytes: int = 512) -> None:
    """
    Initialized server and run it for ever.

    :param host: server host name or ip
    :param port: server port
    :param read_bytes: number of reading bytes
    """
    loop = asyncio.new_event_loop()
    _server = asyncio.start_server(tcp_read_echo(read_bytes), host, port, loop=loop)
    loop.run_until_complete(_server)
    loop.run_forever()


def serverx_in_thread(host: str, port: int, read_bytes: int = 512) -> threading.Thread:
    """
    Run Server in thread.

    :param host: server host name or ip
    :param port: server port
    :param read_bytes: number of reading bytes
    :return: server thread
    """
    thread = threading.Thread(target=serverx, name='server', args=(host, port, read_bytes, ))
    thread.daemon = True
    thread.start()
    return thread
