import asyncio
import pytest
import threading


async def echo_handler(reader, writer):
    data = await reader.read(512)
    writer.write(f'received:{data.decode()!r}'.encode())
    await writer.drain()  # Flow control, see later
    writer.close()


def server(host, port):
    loop = asyncio.new_event_loop()
    server_ = asyncio.start_server(echo_handler, host, port, loop=loop)
    loop.run_until_complete(server_)
    loop.run_forever()


@pytest.fixture(scope='session')
def tcp_server():
    """Run testing tcp server."""
    host, port = 'localhost', 33888
    thread = threading.Thread(target=server, name='server', args=(host, port, ))
    thread.daemon = True
    thread.start()
    yield host, port
