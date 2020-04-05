import os
import random
from typing import Any, Tuple, Union
from PIL import Image, ImageDraw, ImageFont, ImageColor
from . import colors, command, helper

# fetch
def fetch_image(size: Tuple[int, int], color: colors.ColorItem) -> Image:
    # origin_file = os.path.abspath(os.path.dirname(__file__))
    # f = os.path.join(origin_file, "blank.png")
    # print(f)
    # image = Image.open(f)
    image = Image.new("RGB", size, tuple(color.RGB))
    return image

# color


def render_color(image: Image, color: colors.ColorItem) -> Image:
    img = image.copy().convert("RGB")
    size = img.size
    pixdata = img.load()
    for y in range(size[1]):
        for x in range(size[0]):
            pixdata[x, y] = (color.RGB[0], color.RGB[1], color.RGB[2])
    return img

# text


def render_text(
    image: Image,
    text: str,
    origin: Tuple[int, int],
    color: Tuple[int, int, int] = (0, 0, 0),
    font: Union[str, None] = None,
    size: Union[int, None] = None
) -> Image:
    img = image.copy().convert("RGB")
    font = ImageFont.truetype(
        font=font or "grunge_serifia.ttf", size=size or 100)
    draw = ImageDraw.Draw(img)
    print("render text " + str(text))
    draw.text(origin, text, color, font=font)
    return img


# 图片保存
def cache_image(image: Image, file_name: str) -> ImageDraw:
    temp = helper.get_cache_dir()
    path = os.path.join(temp, file_name)
    print("cache image to " + str(path))
    image.save(path)
    return image
