# -*- coding: utf-8 -*-
# @Time     : 2023/9/10 10:48
# @Author   : JiMing
# @File     : bootstrap.py
# @SoftWare : PyCharm
from django import forms


class Bootstrap(forms.ModelForm):
    """
    bootstrap样式类
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 循环查找到所有的插件
        for name, field in self.fields.items():
            if field.widget.attrs:
                # 如果原有标签存在样式 那么我们就添加
                field.widget.attrs['class'] = 'form-control'
                field.widget.attrs['placeholder'] = field.label
            else:
                # 不存在的直接设置
                field.widget.attrs = {'class': 'form-control', 'placeholder': field.label}
