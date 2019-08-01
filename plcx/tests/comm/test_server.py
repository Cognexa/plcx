from plcx.comm.server import serverx_in_thread


def test_server_context(tcp_client):
    """
    Test tcp server object for reading message form client.

    :param tcp_client: function for send message to server
    """
    host, port, client = tcp_client
    serverx_in_thread(host, port, 16)

    response = client(b'test', 4)
    assert response == b'ok'
