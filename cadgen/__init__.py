from .thread_limits import apply_worker_thread_limits

apply_worker_thread_limits()

from . import _addons  # Register the bundled CadQuery geometry helpers.

__version__ = "1.0.0"

__all__ = ["CADGenCli"]


def __getattr__(name: str):
    if name == "CADGenCli":
        from .cli import CADGenCli

        return CADGenCli
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
