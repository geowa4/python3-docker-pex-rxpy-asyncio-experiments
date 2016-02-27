import rx
from rx.subjects import Subject
asyncio = rx.config['asyncio']


class TCPSubject(Subject):
    def __init__(self):
        super().__init__()

    @asyncio.coroutine
    def handle_request(self, reader, writer):
        data = yield from reader.readline()
        message = data.decode()
        addr = writer.get_extra_info('peername')
        print('Received {} from {}'.format(message.strip(), addr))
        self.on_next((message, addr[0]))

        print('Send: {}'.format(message.strip()))
        writer.write(data)
        yield from writer.drain()

        print('Close the client socket')
        writer.close()
