from typing import List
from captcha.image import ImageCaptcha
import random
import base64


WORDS = [
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
]



def create_code(k: int, *, img_width: int = 100, img_height: int = 50, font_sizes:List[int] = None):
    if not font_sizes:
        font_sizes = [35, 30, 33]
    elif isinstance(font_sizes, int):
        font_sizes = [font_sizes]
    image = ImageCaptcha(width=img_width, height=img_height, font_sizes=font_sizes)
    codes = ''.join(random.choices(WORDS, k=k))
    captcha_img = image.generate(codes)
    return captcha_img.read(), codes


def create_base64_code(k: int, *, img_width: int = 100, img_height: int = 50, font_sizes:List[int] = None):
    captcha_img, codes = create_code(k, img_width=img_width, img_height=img_height, font_sizes=font_sizes)
    return "data:image/png;base64," + base64.b64encode(captcha_img).decode('utf-8'), codes


if __name__ == '__main__':
    print(create_base64_code(4))
