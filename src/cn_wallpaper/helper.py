
import os, sys
import logging
from typing import Tuple, Union

# config Option
clean_cache_dir: bool = False

# helpers

def cache_pid():
    pid = os.getpid()
    with open('pid.log', 'w') as f:
        f.write(str(pid))

def query_pid() -> Union[None, int]:
    fn = 'pid.log'
    if not os.path.exists(fn):
        return None
    with open(fn, 'r') as f:
        return int(f.read())



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
    if not path: os.rmdir(dir)


def safe_origin(
    want_origin: Tuple[int, int], 
    max_size: Tuple[int, int], 
    content_size: Tuple[int, int], 
) -> Tuple[int, int]:
    # width, height
    target_x: int
    target_y: int
    target_x = min(max(100, want_origin[0]), max_size[0] - content_size[0] - 100)
    target_y = min(max(100, want_origin[1]), max_size[1] - content_size[1] - 100)
    return (target_x, target_y)


# log
def sprint(text: str) -> str:
    return text

def print_err(text: str):
    sys.stderr.write(sprint(text) + "\n")

def print_log(text: str):
    sys.stdout.write(sprint(text) + "\n")