import sys
import time
import io
from contextlib import redirect_stdout
from typing import Any, Dict


class Logger:
    """
    Minimal-overhead ANSI logger for real-time services.
    """
    __slots__ = ("header", "_prefix")

    _COLORS: Dict[str, str] = {
        "LOG": "",
        "SUCCESS": "\033[32m",
        "WARNING": "\033[33m",
        "ERROR": "\033[31m",
        "RESET": "\033[0m",
    }

    def __init__(self, header: str = "Default") -> None:
        self.header = header
        self._prefix = f"[{header}]"

    def _write(
        self,
        level: str,
        msg: str,
        *args: Any,
        subheader: str | None = None,
        **kw: Any,
    ) -> None:
        color = self._COLORS[level]
        reset = self._COLORS["RESET"]
        head = f"{color}{self._prefix}"
        if subheader:
            head += f"[{subheader}]"
        head += " "

        if not args and not kw:
            sys.stdout.write(f"{head}{msg}{reset}\n")
            return

        parts: list[str] = [msg]
        if args:
            parts.extend(map(str, args))
        if kw:
            parts.extend(f"| {k}={v}" for k, v in kw.items())
        sys.stdout.write(f"{head}{' '.join(parts)}{reset}\n")

    # public
    def log(self, msg: str='', *a, subheader=None, **k):     self._write("LOG",     msg, *a, subheader=subheader, **k)
    def success(self, msg: str='', *a, subheader=None, **k): self._write("SUCCESS", msg, *a, subheader=subheader, **k)
    def warning(self, msg: str='', *a, subheader=None, **k): self._write("WARNING", msg, *a, subheader=subheader, **k)
    def error(self, msg: str='', *a, subheader=None, **k):   self._write("ERROR",   msg, *a, subheader=subheader, **k)

# ───────────────────────── Benchmark helper ────────────────────────────────────
def run_cases(LoggerCls):
    srv = LoggerCls("Srv")
    srv.log("boot OK")
    srv.success("client connected", "192.168.1.42", subheader="Net")
    srv.warning("latency", 240, "ms", subheader="Net")
    srv.error("timeout", peer="192.168.1.42", subheader="Net")

    auth = LoggerCls("Auth")
    auth.log("login", user="alice")
    auth.success("jwt issued", user="alice")
    auth.warning("passwd retry", user="bob", left=2)
    auth.error("account lock", user="eve", reason="too many retries")



if __name__ == "__main__":
    REPEAT = 10_000  # adjust for your machine

    show_examples = True
    if show_examples:
        print('\n== Examples ==\n')
        srv = Logger("Srv")
        srv.log("boot OK")
        srv.success("client connected", "192.168.1.42", subheader="Net")
        srv.warning("latency", 240, "ms", subheader="Net")
        srv.error("timeout", peer="192.168.1.42", subheader="Net")

        auth = Logger("Auth")
        auth.log("login", user="alice")
        auth.success("jwt issued", user="alice")
        auth.warning("passwd retry", user="bob", left=2)
        auth.error("account lock", user="eve", reason="too many retries")
