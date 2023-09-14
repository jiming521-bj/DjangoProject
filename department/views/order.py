# -*- coding: utf-8 -*-
# @Time     : 2023/9/13 11:39
# @Author   : JiMing
# @File     : order.py
# @SoftWare : PyCharm
import json
import random

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, HttpResponse, redirect
from department.my_forms import OrderModelForm
from django.http import JsonResponse
from datetime import datetime
from department import models
from department.utils import myPage


def order_list(request):
    """
    订单列表
    :param request:
    :return:
    """
    # 获取订单表中的所有数据值
    querySet = models.Order.objects.all()

    # 实现分页功能
    page_object = myPage.pagination(request, querySet, page_size=10)

    # 实例化OrderModelForm 获取输入框
    forms = OrderModelForm()
    context = {
        'forms': forms,
        'querySet': page_object.pageQuerySet,
        'page_html': page_object.html(),
    }
    return render(request, 'order-list.html', context)


@csrf_exempt
def order_add(request):
    """
    添加订单
    :param request:
    :return:
    """
    # 获取OrderModelForm对象
    forms = OrderModelForm(data=request.POST)
    if forms.is_valid():
        # 保存数据
        # 因为订单编号不需要用户输入 系统自定生
        forms.instance.order_id = datetime.now().strftime('%y%m%d%H%M%S') + str(random.randint(1000, 9999))

        # 获取登录后的用户ID作为订单处理者保存到数据库中
        forms.instance.person_id = request.session['info'].get('id')

        # 保存到数据库中
        forms.save()
        context = {'static': True}
        return JsonResponse(context)
    context = {
        'static': False,
        'error': forms.errors
    }
    return HttpResponse(json.dumps(context))


def order_detail(request):
    """
    修改数据
    :param request:
    :return:
    """
    # 获取修改数据的nid
    nid = request.GET.get('nid')

    if not models.Order.objects.filter(id=nid).exists():
        context = {
            'static': False,
            'error': '该条数据不存在，修改失败!',
        }
        return HttpResponse(json.dumps(context))
    # 方式一
    # row_query = models.Order.objects.filter(id=nid).first()
    # context = {
    #     'static': True,
    #     'data': {
    #         'order_name': row_query.order_name,
    #         'order_price': row_query.order_price,
    #         'order_static': row_query.order_static,
    #     }
    # }

    # 方式二
    row_query = models.Order.objects.filter(id=nid).values('order_name', 'order_price', 'order_static').first()
    context = {
        'static': True,
        'data': row_query,
    }
    return JsonResponse(context)


@csrf_exempt
def order_edit(request):
    """
    修改数据
    :param request:
    :return:
    """
    nid = request.GET.get('nid')
    print(nid)
    # 判断改条数据是否存在
    exist = models.Order.objects.filter(id=nid).first()
    if not exist:
        context = {
            'static': False,
            'tips': '数据不存在'
        }
        return JsonResponse(context)
    forms = OrderModelForm(data=request.POST, instance=exist)
    if forms.is_valid():
        forms.save()
        context = {
            'static': True,
        }
        return HttpResponse(json.dumps(context))
    context = {
        'static': False,
        'error': forms.errors
    }
    return HttpResponse(json.dumps(context))


def order_delete(request):
    """
    删除数据
    :param request:
    :return:
    """
    if request.method == 'GET':
        # 判断传递的nid是否存在
        nid = request.GET.get('nid')
        if not models.Order.objects.filter(id=nid).exists():
            context = {'static': False, 'error': '数据不存在，删除失败!'}
            return JsonResponse(context)
        models.Order.objects.filter(id=nid).delete()
        context = {'static': True, 'mes': '删除成功'}
        return HttpResponse(json.dumps(context))
