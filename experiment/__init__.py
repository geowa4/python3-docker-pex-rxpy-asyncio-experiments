import rx
from rx.concurrency import AsyncIOScheduler
from rx.observable import Observable
from .tcpserver import TCPServer
from .simpleobserver import SimpleObserver
asyncio = rx.config['asyncio']


def run(interval, port):
    scheduler = AsyncIOScheduler()
    clock = Observable.timer(0, interval, scheduler=scheduler)
    loop = asyncio.get_event_loop()
    server = TCPServer(loop)
    observer = SimpleObserver()

    all_events = server.tcp_subject.map(
        lambda x: x[0].strip()
    ).merge(clock)
    all_events.subscribe(observer)

    server.start(port)
    loop.close()
