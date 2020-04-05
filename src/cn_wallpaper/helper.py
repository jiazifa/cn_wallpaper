
import os
import logging
from typing import Tuple

# config Option
clean_cache_dir: bool = False

# helpers


def get_home_dir() -> str:
    return os.environ.get("HOME") or ""


def get_cache_dir():
    home = get_home_dir()
    path = os.path.join(home, ".wallpaper")
    if not os.path.exists(path):
        os.mkdir(path)
    return path


def get_file_from_cache(file: str) -> str:
    return os.path.join(get_cache_dir(), file)


def clean_cache_except(path: str):
    dir = get_cache_dir()
    for f in os.listdir(dir):
        if f == path:
            continue
        os.remove(os.path.join(dir, f))


def safe_origin(
    want_origin: Tuple[int, int], 
    max_size: Tuple[int, int], 
    content: str, 
    font_size: int
) -> Tuple[int, int]:
    # width, height

    width = 0
    height = font_size
    for c in content:
        if c.isalpha:
            width += int(font_size / 2)
        else:
            width += font_size
    target_x: int
    target_y: int
    target_x = min(max(0, want_origin[0]), max_size[0] - width)
    target_y = min(max(0, want_origin[1]), max_size[1] - height)
    return (target_x, target_y)
