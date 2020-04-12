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
from argparse import ArgumentParser, Namespace
from multiprocessing import Process, Queue
from typing import Tuple, Any, Dict, List, Callable, Optional, Union
from cn_wallpaper import colors, command, render, helper


def execute_by_command(args: Namespace):
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
    font_direction: Union[None, str] = args.direction
    payload_size: Tuple[int, int]
    origin: Tuple[int, int]

    font = command.fetch_font(font_name=args.font)
    color = random.choice(colors.load_colors())

    font_size = int(args.size or 140)
    font_path = font.path
    display_font: render.ImageFont = render.fetch_font(font_path, font_size)

    if args.rgb:
        background_color_rgb = (int(i) for i in args.rgb.split(","))
        content = ""
    else:
        background_color_rgb = color.RGB
        render_content = color.name

    if args.content:
        print(args.content)
        render_content = render_content.join(args.content)
        print(render_content)
    elif args.input:
        with open(args.input) as f:
            render_content = f.read()

    if args.origin:
        origin = (int(i) for i in args.origin.split(","))
    else:
        origin = (300, 200)

    payload_size = command.bounds_of_window()

    img = render.fetch_image(payload_size, background_color_rgb)
    
    temp_filename = str("{}.png".format(uuid.uuid4().hex))
    font_bounds = render.size_of_text(img, render_content, display_font, font_direction)
    origin = helper.safe_origin(origin, payload_size, font_bounds)
    rgb = (255, 255, 255)
    img = render.render_text(img, render_content, origin, rgb, display_font)
    img = render.cache_image(img, temp_filename)
    command.set_cache_wallpaper(temp_filename)

def is_running() -> bool:
    if not helper.query_pid():
        return False
    pid = helper.query_pid()
    return pid in command.get_pids()

def run_background(queue: Queue):
    print('running background')
    if not helper.query_pid():
        helper.cache_pid()
    
    pid = helper.query_pid()
    print(pid)
    print(command.get_pids())
    if pid and pid in command.get_pids():
        print('paper is already running？')
        return
    else:
        helper.cache_pid()
    while True:
        value = queue.get(True)
        execute_by_command(value)


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
        "-c",
        "--clean",
        action="store_true",
        help="clean files after set wallpaper"
    )

    # 字体选项
    font_group = parser.add_argument_group("Font Option")
    font_group.add_argument(
        "--direction",
        help="direction of render content"
    )
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

    content_group = parser.add_argument_group("Content Option")
    content_group.add_argument(
        "-i",
        "--input",
        help="input file for render content"
    )
    content_group.add_argument(
        "--origin",
        help="origin of render content"
    )

    parser.add_argument("content", nargs="*", help=argparse.SUPPRESS)

    args = parser.parse_args()
    execute_by_command(args)
    


def main(**kwargs):
    parser_main(**kwargs)
