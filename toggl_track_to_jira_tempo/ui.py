"""
Interactive terminal choice picker (arrow keys) with a numeric fallback
for non-TTY contexts (pipes, tests, cron).

Renders to stderr to stay correctly ordered with the Logger output, reads
keys from stdin in raw mode. Selected option is highlighted; number keys
select directly; arrow keys move the highlight; Enter confirms.
"""
import shutil
import sys

from utils import Logger

try:
    import termios
    import tty
    _TERMIOS_AVAILABLE = True
except ImportError:
    _TERMIOS_AVAILABLE = False

_K_UP = "\x1b[A"
_K_DOWN = "\x1b[B"
_K_ENTER = ("\r", "\n")
_K_CTRL_C = "\x03"


def interactive_available() -> bool:
    if not _TERMIOS_AVAILABLE:
        return False
    try:
        return sys.stdin.isatty() and sys.stderr.isatty()
    except Exception:
        return False


class _RawMode:
    def __enter__(self):
        self._fd = sys.stdin.fileno()
        self._old = termios.tcgetattr(self._fd)
        tty.setraw(self._fd)
        return self

    def __exit__(self, *exc_info):
        termios.tcsetattr(self._fd, termios.TCSADRAIN, self._old)


def _terminal_width() -> int:
    try:
        return shutil.get_terminal_size(fd=sys.stderr.fileno()).columns
    except Exception:
        return 80


def _read_key() -> str:
    ch = sys.stdin.read(1)
    if ch == "\x1b":
        seq = sys.stdin.read(2)
        if seq == "[A":
            return _K_UP
        if seq == "[B":
            return _K_DOWN
        return ""
    if ch in _K_ENTER:
        return _K_ENTER[0]
    if ch == _K_CTRL_C:
        raise KeyboardInterrupt
    return ch


def _render(choices, selected, width):
    lines = []
    for i, choice in enumerate(choices):
        text = choice
        if len(text) > width - 7:
            text = text[: width - 10] + "..."
        marker = "> " if i == selected else "  "
        color = "\x1b[1;96m" if i == selected else Logger.INFO_SECONDARY
        lines.append(f"{marker}{color}{text}\x1b[0m")
    return lines


def arrow_select(prompt: str, choices: list) -> str:
    """Arrow-key selection over `choices`. Returns the selected choice."""
    width = _terminal_width()
    selected = 0
    rendered = None

    sys.stderr.write(prompt + "\n")
    sys.stderr.flush()

    try:
        with _RawMode():
            sys.stderr.write("\x1b[?25l")  # hide cursor
            while True:
                new_lines = _render(choices, selected, width)
                if rendered is None:
                    for line in new_lines:
                        sys.stderr.write(line + "\r\n")
                else:
                    sys.stderr.write(f"\x1b[{len(choices)}A")
                    for line in new_lines:
                        sys.stderr.write("\x1b[2K" + line + "\r\n")
                sys.stderr.flush()
                rendered = new_lines

                key = _read_key()
                if key == _K_UP:
                    selected = (selected - 1) % len(choices)
                elif key == _K_DOWN:
                    selected = (selected + 1) % len(choices)
                elif key in _K_ENTER:
                    break
                elif key.isdigit() and key != "0":
                    idx = int(key) - 1
                    if 0 <= idx < len(choices):
                        selected = idx
                        break
        return choices[selected]
    finally:
        sys.stderr.write("\x1b[?25h")  # show cursor
        sys.stderr.flush()