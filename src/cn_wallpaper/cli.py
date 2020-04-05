#! -*- coding: utf-8 -*-

import re
import os
import sys
import io
import uuid
import json
import time
import argparse
import logging, random
from argparse import ArgumentParser
from typing import Tuple, Any, Dict, List, Callable, Optional, Union
from cn_wallpaper import colors, command, render

def parser_main(**kwargs):
    logging.basicConfig(format="[%(levelname)s] %(message)s")

    parser: ArgumentParser = ArgumentParser(
        prog="paper",
        usage="paper [OPTION]",
        description="china colors wallpaper"
    )
    parser.add_argument("-v", "--version", action="version")
    # 设置图片桌面
    parser.add_argument("-f", "--file", action="store_true")
     # 文件或者文件夹路径
    parser.add_argument("file_or_direct", nargs="*")

    args = parser.parse_args()
    # filepath = args.file_or_direct[0]
    # if args.file:
    #     common.set_wallpaper(filepath)
    # else:
    #     common.set_wallpaper_dir(filepath)
    color = random.choice(colors.load_colors())
    img = render.fetch_image(command.bounds_of_window(), color)
    
    font = command.fetch_font()
    f = str("{}.png".format(uuid.uuid4().hex))
    rgb = (255, 255, 255)
    img = render.render_text(img, color.name, (200, 200), rgb, font.path, 140)
    img = render.render_text(img, color.pinyin, (200, 360), rgb, font.path, 50)
    img = render.cache_image(img, f)
    command.set_cache_wallpaper(f)
    
    


def main(**kwargs):
    parser_main(**kwargs)
