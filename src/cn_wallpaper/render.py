import os
import random
from typing import Any, Tuple, Union
from PIL import Image, ImageDraw, ImageFont, ImageColor
from . import colors, command, helper

# fetch
def fetch_image(size: Tuple[int, int], color: Tuple[int, int, int]) -> Image:
    image = Image.new("RGB", size, tuple(color))
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
def size_of_text(
    image: Image, 
    text: str, 
    font: ImageFont,
    direction: Union[None, str]=None
) -> Tuple[int, int]:
    draw = ImageDraw.Draw(image)
    size = draw.multiline_textsize(text, font) #, direction=direction or "ltr")
    return size

def fetch_font(font_path: str, font_size: int) -> ImageFont:
    return ImageFont.truetype(font=font_path, size=font_size, layout_engine=ImageFont.LAYOUT_RAQM)

def render_text(
    image: Image,
    text: str,
    origin: Tuple[int, int],
    color: Tuple[int, int, int] = (0, 0, 0),
    font = None
) -> Image:
    img = image.copy().convert("RGB")
    render_font = font or ImageFont.truetype(
        font=font)
    draw = ImageDraw.Draw(img)
    draw.multiline_text(origin, text, color, font=font)
    return img


# 图片保存
def cache_image(image: Image, file_name: str) -> ImageDraw:
    temp = helper.get_cache_dir()
    path = os.path.join(temp, file_name)
    image.save(path)
    return image
