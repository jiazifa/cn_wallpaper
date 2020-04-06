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
        helper.clean_cache_except("")
        helper.print_log("Cache cleared")
        return
    
    render_content: str
    background_color_rgb: Tuple[int, int, int]
    font_name: str
    font_size: int
    font_path: str
    payload_size: Tuple[int, int]

    font = command.fetch_font(font_name=args.font)
    color = random.choice(colors.load_colors())

    font_size = int(args.size or 140)
    font_path = font.path

    if args.rgb:
        background_color_rgb = (int(i) for i in args.rgb.split(","))
        content = ""
    else:
        background_color_rgb = color.RGB
        render_content = color.name

    if args.content:
        render_content = render_content.join(args.content)

    payload_size = command.bounds_of_window()

    img = render.fetch_image(payload_size, background_color_rgb)
    
    temp_filename = str("{}.png".format(uuid.uuid4().hex))
    ori = (random.randint(0, payload_size[0]), random.randint(0, payload_size[1]))
    origin = helper.safe_origin(ori, payload_size, render_content, font_size)
    rgb = (255, 255, 255)
    img = render.render_text(img, render_content, origin, rgb, font_path, font_size)
    img = render.cache_image(img, temp_filename)
    command.set_cache_wallpaper(temp_filename)
    
    


def main(**kwargs):
    parser_main(**kwargs)
