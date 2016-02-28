import argparse
from . import run


parser = argparse.ArgumentParser(
    description='Experiment with RxPY and asyncio.'
)
parser.add_argument(
    '--interval', type=int, default=1000*60,
    help='Resync interval'
)
parser.add_argument(
    '--tcp-port', type=int, default=8888,
    help='TCP server port'
)
args = parser.parse_args()
run(
    args.interval,
    args.tcp_port,
)
