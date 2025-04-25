import random
import string
import uuid
from datetime import datetime, timedelta

from PIL import Image, ImageDraw, ImageFont, ImageFilter
from flask import current_app

from common.service.redis_client import redis

CAPTCHA_PREFIX = 'captcha:'


def generate_captcha(size=(120, 40),
                     chars=string.ascii_uppercase + string.digits,
                     length=4,
                     bg_color=(255, 255, 255),
                     font_size=28,
                     font_path='arial.ttf',
                     draw_lines=True,
                     line_num=3,
                     draw_points=True,
                     point_chance=2):
    """
    生成验证码图片
    参数：
        size: 图片尺寸，默认(120, 40)
        chars: 允许的字符集合，默认大写字母和数字
        length: 验证码长度，默认4个字符
        bg_color: 背景颜色，默认白色
        font_size: 字体大小
        font_path: 字体文件路径，默认arial.ttf
        draw_lines: 是否画干扰线
        line_num: 干扰线数量
        draw_points: 是否画干扰点
        point_chance: 干扰点出现的概率，0-100
    """

    width, height = size
    img = Image.new('RGB', size, bg_color)
    draw = ImageDraw.Draw(img)

    def create_lines():
        """绘制干扰线"""
        for _ in range(line_num):
            begin = (random.randint(0, width), random.randint(0, height))
            end = (random.randint(0, width), random.randint(0, height))
            draw.line([begin, end], fill=get_random_color(), width=2)

    def create_points():
        """绘制干扰点"""
        for w in range(width):
            for h in range(height):
                if random.randint(0, 100) < point_chance:
                    draw.point((w, h), fill=get_random_color())

    def get_random_color():
        """生成随机颜色"""
        return (random.randint(32, 127),
                random.randint(32, 127),
                random.randint(32, 127))

    # 生成验证码字符串
    captcha = ''.join(random.choice(chars) for _ in range(length))

    try:
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        font = ImageFont.load_default()

    # 绘制文字
    x = 5
    for char in captcha:
        # 每个字符随机颜色、位置微调
        y = random.randint(0, height - font_size)
        draw.text((x, y),
                  char,
                  font=font,
                  fill=get_random_color())
        x += (width - 10) // length  # 字符间距

    if draw_lines:
        create_lines()
    if draw_points:
        create_points()

    # 添加滤镜效果（可选）
    img = img.filter(ImageFilter.EDGE_ENHANCE)

    captcha_id = str(uuid.uuid4())
    key = CAPTCHA_PREFIX + captcha_id
    value = {
        'code': captcha,
        'created_at': datetime.now().isoformat()
    }
    redis.setex(key, timedelta(minutes=5), str(value))

    return img, captcha, captcha_id


def verify_captcha(user_input, captcha_id):
    key = CAPTCHA_PREFIX + captcha_id
    captcha_data = redis.get(key)
    try:
        captcha_data = eval(captcha_data)
    except Exception as e:
        current_app.logger.error(f"Error parsing captcha data: {e}")
        return False, 'Invalid captcha'

    if not captcha_data:
        return False, 'Captcha expired or invalid'

    server_code = captcha_data.get('code')
    created_at = captcha_data.get('created_at')

    if datetime.now() - datetime.fromisoformat(created_at) > timedelta(minutes=5):
        redis.delete(key)
        return False, 'Captcha expired'

    redis.delete(key)

    if user_input.upper() == server_code.upper():
        return True, 'Success'

    return False, 'Invalid captcha'


# 使用示例
if __name__ == '__main__':
    img, code, captcha_id = generate_captcha()
    img.show()  # 显示图片
    print("验证码:", code)
    # img.save('captcha.jpg')  # 保存图片
