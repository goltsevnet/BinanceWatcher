import sys

# import signal

# signal.signal(signal.SIGINT, signal.SIG_DFL)

from Watcher import Watcher


def main():
    watcher = Watcher()
    watcher.start_watcher("xrpusdt")


if __name__ == "__main__":
    main()
