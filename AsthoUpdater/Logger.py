import time


class Colors(enumerate):
    CYAN = '\033[96m'
    RED = '\033[91m'
    END_LINE = '\033[0m'


class Logger(object):
    def __init__(
            self,
            name: str = None,
            activated: bool = True
    ):
        self.name = name if name is not None else "AsthoUpdater"
        self.activated = activated

    def log(self, log: str):
        if self.activated:
            log = f"[{time.strftime('%H:%M:%S - %d/%m/%Y', time.localtime())}] [{self.name}] [LOG] {log}"
            print(log)

    def warn(self, warn: str):
        if self.activated:
            warn = f"[{time.strftime('%H:%M:%S - %d/%m/%Y', time.localtime())}] [{self.name}] [WARN] {warn}"
            print(Colors.CYAN + warn + Colors.END_LINE)

    def error(self, error: str):
        if self.activated:
            error = f"[{time.strftime('%H:%M:%S - %d/%m/%Y', time.localtime())}] [{self.name}] [ERROR] {error}"
            print(Colors.RED + error + Colors.END_LINE)
