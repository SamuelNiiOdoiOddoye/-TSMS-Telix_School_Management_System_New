"""Window icon setup."""

from __future__ import annotations

import logging
import os
import tkinter as tk
from pathlib import Path

from telix.config import TELIX_ICON_IMAGE_PATH, TELIX_ICON_PATH

LOGGER = logging.getLogger("telix.ui.window")


def apply_window_icon(master: tk.Tk) -> tk.PhotoImage | None:
    """Set the title-bar and taskbar icons while keeping the PNG image alive for the window."""
    if hasattr(master, "_telix_icon_image") and master._telix_icon_image is not None:
        return master._telix_icon_image

    png_path = TELIX_ICON_IMAGE_PATH.resolve()
    ico_path = TELIX_ICON_PATH.resolve()
    LOGGER.info(
        "Resolved icon paths: png=%s (exists=%s), ico=%s (exists=%s)",
        png_path,
        png_path.exists(),
        ico_path,
        ico_path.exists(),
    )

    icon_image = _apply_png_icon(master, png_path)
    _apply_windows_icon(master, ico_path)
    master._telix_icon_image = icon_image
    return icon_image


def _apply_png_icon(master: tk.Tk, png_path: Path) -> tk.PhotoImage | None:
    if not png_path.exists():
        LOGGER.warning("PNG application icon is missing at %s", png_path)
        return None
    try:
        icon_image = tk.PhotoImage(file=str(png_path))
        master.iconphoto(True, icon_image)
        LOGGER.info("Applied PNG window icon from %s", png_path)
        return icon_image
    except tk.TclError:
        LOGGER.exception("Failed to load PNG window icon from %s", png_path)
        return None


def _apply_windows_icon(master: tk.Tk, ico_path: Path) -> None:
    if os.name != "nt":
        return
    if not ico_path.exists():
        LOGGER.warning("Windows ICO icon is missing at %s", ico_path)
        return
    if not _is_valid_ico_file(ico_path):
        LOGGER.warning("Windows ICO file is not a valid ICO image: %s", ico_path)
        return
    try:
        master.iconbitmap(str(ico_path))
        LOGGER.info("Applied Windows taskbar icon from %s", ico_path)
    except tk.TclError:
        LOGGER.exception("Failed to apply Windows iconbitmap for %s", ico_path)


def _is_valid_ico_file(path: Path) -> bool:
    try:
        data = path.read_bytes()
    except OSError:
        LOGGER.warning("Could not read icon file for validation: %s", path)
        return False
    if len(data) < 6:
        return False
    return data[:2] == b"\x00\x00" and data[2:4] == b"\x01\x00" and int.from_bytes(data[4:6], "little") > 0
