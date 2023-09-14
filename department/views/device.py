# -*- coding: utf-8 -*-
# @Time     : 2023/9/12 19:03
# @Author   : JiMing
# @File     : device.py
# @SoftWare : PyCharm

from django.shortcuts import render, HttpResponse,redirect
from django.views.decorators.csrf import csrf_exempt
from department.my_forms import Device_List
from django.http import JsonResponse  # 返回JSON格式的数据
import json
from department import models
from department.utils import myPage


def device_list(request):
    """
    设备管理
    :param request:
    :return:
    """
    # 获取数据库中所有的任务信息
    querySet = models.Device.objects.all()
    # print(request.GET)
    # 分页显示
    page_object = myPage.pagination(request, querySet, page_size=4)
    # 创建Form对象
    forms = Device_List()
    context = {
        'forms': forms,
        'querySet': page_object.pageQuerySet,
        'page_html': page_object.html()
    }
    return render(request, 'device-list.html', context)


@csrf_exempt
def device_ajax(request):
    request_param = request.GET
    print(request_param)

    request_method_post = request.POST
    print(request_method_post)

    # print(request_param.get('name'))
    # print(request_param.get('age'))

    data_list = {
        'name': 'ming',
        'age': 22,
        'gender': '男',
        'hobby': 'basketball',
        'remark': '这是一场没有尽头的旅途'
    }

    # if request_param.get('name') != 'ming':
    #     return HttpResponse('失败了')
    return HttpResponse(json.dumps(data_list))


@csrf_exempt
def device_add(request):
    """
    添加任务
    :param request:
    :return:
    """
    forms = Device_List(data=request.POST)
    if forms.is_valid():
        forms.save()
        data_list = {
            'static': True
        }
        return HttpResponse(json.dumps(data_list))
    # print(forms.errors)
    data_list = {
        'static': False,
        'error': forms.errors
    }
    return HttpResponse(json.dumps(data_list))


def device_delete(request, nid):
    """
    删除
    :param nid:
    :param request:
    :return:
    """
    if request.method == 'GET':
        if not models.Device.objects.filter(id=nid).exists():
            return HttpResponse("<script>alert('数据不存在');window.location='/device/list/'</script>")
        models.Device.objects.filter(id=nid).delete()
        return redirect('/device/list/')


def device_muilt(request):
    """
    文件上传操作
    :param request:
    :return:
    """

    # 获取文件上传的内容
    files = request.FILES.get('files')

    print(files)

    # 返回响应数据
    return HttpResponse("<script>alert('文件上传成功');window.location='/device/list/';</script>")
