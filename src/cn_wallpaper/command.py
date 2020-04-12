
import os
import re
import random
import subprocess
from collections import namedtuple
from typing import List, Tuple, Union
from . import helper

FontSpec = namedtuple("FontSpec", ["path", "name"])

def get_pids() -> List[int]:
    command = """
    ps | cut -d ' ' -f 2
    """
    result = execute_want_return_value(command)
    rs = []
    for r in result:
        if len(r) == 0:
            continue
        rs.append(int(r))
    return list(set(rs))

def fetch_font_list() -> List[FontSpec]:
    command = """
    export LC_CTYPE="en_US.UTF-8" | fc-list :lang=zh-cn | grep -e "ttc" -e "otf" -e "woff" -e "eot" -e "svg"
    """
    result = execute_want_return_value(command)
    font_list: List[FontSpec] = []
    for f in result:
        path = f.strip().split(":")[0]
        name = path.split("/")[-1].lower()
        font_list.append(FontSpec(path, name))
    return font_list


def fetch_font(fonts: Union[None, List[FontSpec]] = None, font_name: Union[None, str] = None) -> FontSpec:
    font_list = fonts or fetch_font_list()
    font = random.choice(font_list)
    if font_name:
        fs = list(filter(lambda font: font.name == font_name, font_list))
        if fs and len(fs) > 0:
            font = fs[0]
    return font


def set_wallpaper_dir(dir: str):
    all_files: list = []
    for file in os.listdir(dir):
        all_files.append(os.path.join(dir, file))
    file = random.choice(all_files)
    set_wallpaper(file)


def set_cache_wallpaper(filename: str):
    path = helper.get_file_from_cache(filename)
    set_wallpaper(path)
    
    if helper.clean_cache_dir:
        helper.clean_cache_except(filename)


def set_wallpaper(filepath: str):
    command: str = """
    osascript -e "tell application \\"Finder\\" to set desktop picture to POSIX file \\"{}\\""
    """.format(filepath)
    execute_command(command)


def bounds_of_window() -> Tuple[int, int]:
    # command = """
    # osascript -e 'tell application \"Finder\" to get bounds of window of desktop'
    # """
    command = """
    system_profiler SPDisplaysDataType | grep -e \"Resolution\" -e \"Main Display\"
    """
    result = execute_want_return_value(command)
    size: Tuple[int, ...]
    for r in result:
        if r.startswith("Main Display"):
            break
        size = tuple(map(lambda i: int(i), filter(
            None, re.findall(r'\d*', r))))
    return (size[0], size[1])


def execute_command(command: str):
    os.system(command)


def execute_want_one_line(command: str) -> str:
    r = execute_want_return_value(command)
    return r[0]


def execute_want_return_value(command: str) -> List[str]:
    res = subprocess.Popen(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
    out = res.stdout
    if not out:
        return []
    result = out.readlines()
    return list(map(lambda r: str(r, encoding="utf-8").strip(), result))

