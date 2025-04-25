import random
import string


def generate_random_string(length=6):
    """生成随机字母数字组合"""
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for _ in range(length))
