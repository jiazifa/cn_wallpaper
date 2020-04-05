
import os
import logging

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
