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
from cn_wallpaper import colors, command, render, helper


def parser_main(**kwargs):
    logging.basicConfig(format="[%(levelname)s] %(message)s")

    parser: ArgumentParser = ArgumentParser(
        prog="paper",
        usage="paper [OPTION]",
        description="china colors wallpaper"
    )
    parser.add_argument("-v", "--version", action="version")
    # 后台运行选项
    background_grp = parser.add_argument_group("Background Option")
    background_grp.add_argument(
        "-d",
        "--background",
        action="store_true",
        help="application run as background task"
    )
    background_grp.add_argument(
        "-c",
        "--clean",
        action="store_true",
        help="clean files after set wallpaper"
    )

    # 字体选项
    font_group = parser.add_argument_group("Font Option")
    font_group.add_argument(
        "-f",
        "--font",
        help="path for font"
    )
    font_group.add_argument(
        "-s",
        "--size",
        help="font size"
    )
    font_group.add_argument(
        "--rgb",
        help="rgb color as 255,255,255"
    )

    parser.add_argument("content", nargs="*", help=argparse.SUPPRESS)

    args = parser.parse_args()

    # parser
    if args.clean:
        clean_cache_dir = args.clean
    
    font = command.fetch_font(font_name=args.font)
    font_size = int(args.size or 140)
    color = random.choice(colors.load_colors())
    bg_color = color.RGB
    if args.rgb:
        bg_color = (int(i) for i in args.rgb.split(","))
    # diaplay content
    content: str = font.name
    if args.content:
        content = content.join(args.content)
    bounds = command.bounds_of_window()

    img = render.fetch_image(bounds, bg_color)
    
    f = str("{}.png".format(uuid.uuid4().hex))
    ori = (random.randint(0, bounds[0]), random.randint(0, bounds[1]))
    origin = helper.safe_origin(ori, bounds, content, font_size)
    rgb = (255, 255, 255)
    img = render.render_text(img, content, origin, rgb, font.path, font_size)
    img = render.cache_image(img, f)
    command.set_cache_wallpaper(f)
    
    


def main(**kwargs):
    parser_main(**kwargs)
