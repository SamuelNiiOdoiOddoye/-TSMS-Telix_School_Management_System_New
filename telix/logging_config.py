"""Configure privacy-conscious application logging and crash diagnostics."""

from __future__ import annotations

import logging
import sys
import threading
import traceback
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from telix import __version__
from telix.config import APP_DATA_DIR, ISSUE_LOG_DIR, TELIX_LOG_FILE

LOGGER = logging.getLogger("telix")


def configure_logging() -> None:
    """Log operational events to stderr and a local session log without record values."""
    logger = logging.getLogger("telix")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    if logger.handlers:
        return

    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s"))
    logger.addHandler(handler)

    APP_DATA_DIR.mkdir(parents=True, exist_ok=True)
    TELIX_LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    file_handler = logging.FileHandler(TELIX_LOG_FILE, encoding="utf-8")
    file_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s"))
    logger.addHandler(file_handler)


def _safe_issue_log_dir() -> Path:
    ISSUE_LOG_DIR.mkdir(parents=True, exist_ok=True)
    return ISSUE_LOG_DIR


def create_diagnostic_report(
    *,
    source: str,
    exc_info: tuple[type[BaseException], BaseException, Any] | None = None,
    message: str | None = None,
) -> Path | None:
    """Write a local crash/diagnostic report without including school-record JSON data."""
    try:
        report_dir = _safe_issue_log_dir()
    except OSError:
        return None

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    report_path = report_dir / f"crash_{timestamp}_{source.replace(' ', '_')}.txt"

    lines = [
        "Telix diagnostic report",
        f"timestamp_utc: {datetime.now(timezone.utc).isoformat()}",
        f"version: {__version__}",
        f"source: {source}",
        f"python_version: {sys.version.split()[0]}",
        f"platform: {sys.platform}",
    ]
    if message:
        lines.append("")
        lines.append("Summary:")
        lines.append(message)

    if exc_info is not None:
        exc_type, exc_value, exc_tb = exc_info
        lines.extend(["", "Traceback:"])
        lines.extend(traceback.format_exception(exc_type, exc_value, exc_tb))

    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return report_path


def report_exception(
    exc_type: type[BaseException],
    exc_value: BaseException,
    exc_traceback: Any,
    *,
    source: str,
) -> Path | None:
    """Write a crash report and return the saved path so the UI can display it."""
    report_path = create_diagnostic_report(
        source=source,
        exc_info=(exc_type, exc_value, exc_traceback),
    )
    LOGGER.exception("Unhandled %s exception: %s", source, exc_value)
    return report_path


def install_exception_hooks(root: Any | None = None) -> None:
    """Capture Tk callback and unhandled Python exceptions for local bug reports."""
    previous_hook = sys.excepthook

    def _notify_user(path: Path | None, exc_value: BaseException) -> None:
        if root is None or path is None:
            return
        try:
            from tkinter import messagebox

            messagebox.showerror(
                "Telix encountered an unexpected error",
                f"Telix saved a diagnostic report to:\n{path}\n\n"
                "Please review it before sharing it.",
                parent=root,
            )
        except Exception:
            pass

    def _handle_sys_exception(
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_traceback: Any,
    ) -> None:
        report_path = report_exception(exc_type, exc_value, exc_traceback, source="application")
        _notify_user(report_path, exc_value)
        if previous_hook is not None:
            previous_hook(exc_type, exc_value, exc_traceback)

    def _handle_thread_exception(args: threading.ExceptHookArgs) -> None:
        report_path = report_exception(args.exc_type, args.exc_value, args.exc_traceback, source="thread")
        _notify_user(report_path, args.exc_value)

    sys.excepthook = _handle_sys_exception
    threading.excepthook = _handle_thread_exception

    if root is not None:
        root.report_callback_exception = (  # type: ignore[attr-defined]
            lambda exc_class, exc_val, exc_tb: _notify_user(
                report_exception(exc_class, exc_val, exc_tb, source="tkinter callback"),
                exc_val,
            )
        )


__all__ = [
    "configure_logging",
    "create_diagnostic_report",
    "install_exception_hooks",
    "report_exception",
]
