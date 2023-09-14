# -*- coding: utf-8 -*-
# @Time     : 2023/9/14 12:51
# @Author   : JiMing
# @File     : upload.py
# @SoftWare : PyCharm

from django.shortcuts import render, HttpResponse
import os

def upload_list(request):
    """
    文件上传列表
    :param request:
    :return:
    """
    return render(request, 'upload-list.html')


def upload_value(request):
    """
    上传文件的获取
    :param request:
    :return:
    """
    print(request.POST)
    print(request.POST.get('username'))
    print(request.POST.get('userAge'))

    # 获取上传文件的对象
    print(request.FILES.get('files'))

    # 打开文件 写入到项目中
    # files_option = open('jiming.png', mode='wb')
    # for file in request.FILES.get('files'):
    #     files_option.write(file)
    # # 关闭文件
    # files_option.close()

    files_object = request.FILES.get('files')
    with open(files_object.name, 'wb') as files:
        for files_value in files_object.chunks():
            files.write(files_value)

    return HttpResponse("<script>alert('文件上传成功');window.location='/upload/list/'</script>;")
