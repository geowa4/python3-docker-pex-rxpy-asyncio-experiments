import rx
from rx.concurrency import AsyncIOScheduler
from rx.observable import Observable
from .tcpserver import TCPServer
from .simpleobserver import SimpleObserver
asyncio = rx.config['asyncio']


def run(interval, port):
    scheduler = AsyncIOScheduler()
    clock = Observable.interval(interval, scheduler=scheduler)
    server = TCPServer(asyncio.get_event_loop())
    observer = SimpleObserver()

    all_events = clock.merge(server.tcp_subject)
    all_events.subscribe(observer)

    server.start(port)
