import rx
from .tcpsubject import TCPSubject
asyncio = rx.config['asyncio']


class TCPServer:
    def __init__(self, loop):
        self.loop = loop
        self.tcp_subject = TCPSubject()

    def start(self, port):
        server = self.loop.run_until_complete(asyncio.start_server(
            self.tcp_subject.handle_request, '0.0.0.0', port, loop=self.loop
        ))

        # Serve requests until Ctrl+C is pressed
        print('Serving on {}'.format(server.sockets[0].getsockname()))
        try:
            self.loop.run_forever()
        except KeyboardInterrupt:
            pass

        # Close the server
        server.close()
        self.loop.run_until_complete(server.wait_closed())
