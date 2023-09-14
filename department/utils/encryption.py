# -*- coding: utf-8 -*-
# @Time     : 2023/9/10 16:41
# @Author   : JiMing
# @File     : encryption.py
# @SoftWare : PyCharm

from django.conf import settings
import hashlib


def md5(data_string):
    """
    对字符串加密
    :param data_string:
    :return:
    """
    obj = hashlib.md5(settings.SECRET_KEY.encode('utf-8'))  # 加入随机值
    obj.update(data_string.encode('utf-8'))

    return obj.hexdigest()
