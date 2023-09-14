# -*- coding: utf-8 -*-
# @Time     : 2023/9/10 15:18
# @Author   : JiMing
# @File     : admin.py
# @SoftWare : PyCharm
import json

from django.shortcuts import render, HttpResponse, redirect
from department import models
from department.utils import myPage
from department.my_forms import AdminModelForm, AdminEditModelForm, AdminResetModelForm, Login


def admin_list(request):
    """
    管理员列表
    :param request:
    :return:
    """
    # 判断用户之前是否登录过
    # 获取session值
    # info = request.session.get('info')
    # if not info:
    #     return HttpResponse("<script>alert('请先登录后操作');window.location='/login/';</script>")

    search_dict = {}
    # 获取搜索词
    search_value = request.GET.get('q', '')
    if search_value:
        search_dict['username__contains'] = search_value

    # 获取搜索的值 在数据库中进行查找
    querySet = models.Admin.objects.filter(**search_dict).order_by('-username')

    # 获取分页数据
    admin_object = myPage.pagination(request, querySet, page_size=5)

    context = {
        'querySet': admin_object.pageQuerySet,
        'search_value': search_value,
        'admin_page_html': admin_object.html(),
    }
    return render(request, 'admin-list.html', context)


def admin_add(request):
    """
    添加管理员
    :param request:
    :return:
    """
    # 设置标题
    title = '添加管理员'

    if request.method == 'GET':
        forms = AdminModelForm()
        return render(request, 'public-add.html', {'forms': forms, 'title': title})

    # 如果是POST请求 验证密码

    forms = AdminModelForm(data=request.POST)
    context = {
        'forms': forms,
        'title': title,
    }
    if forms.is_valid():
        # 保存数据
        forms.save()
        return HttpResponse("<script>alert('添加成功'); window.location='/login/';</script>")
    return render(request, 'public-add.html', context)


def admin_edit(request, nid):
    """
    修改用户名
    :param nid:
    :param request:
    :return:
    """
    # 判断当前修改的数据是否存在
    exist_querySet = models.Admin.objects.filter(id=nid).first()
    if not exist_querySet:
        return render(request, 'error.html', {'msg': '数据不存在'})

    title = '修改用户名'
    if request.method == 'GET':
        form = AdminEditModelForm(instance=exist_querySet)
        return render(request, 'public-add.html', {'forms': form, 'title': title})

    # 处理POST请求
    form = AdminEditModelForm(data=request.POST, instance=exist_querySet)
    if form.is_valid():
        form.save()
        return HttpResponse("<script>alert('修改成功, 请重新登录');window.location='/login/';</script>")
    return render(request, 'public-add.html', {'forms': form, 'title': title})


def admin_delete(request, nid):
    """
    删除管理员账号
    :param request:
    :param nid:
    :return:
    """
    delete_querySet = models.Admin.objects.filter(id=nid).first()
    if not delete_querySet:
        return render(request, 'error.html', {'msg': '该数据不存在，删除失败！'})

    delete_querySet.delete()
    return redirect('/admin/list/')


def admin_reset(request, nid):
    """
    重置密码
    :param request:
    :param nid:
    :return:
    """
    title = '重置密码'
    reset_querySet = models.Admin.objects.filter(id=nid).first()
    if not reset_querySet:
        return render(request, 'error.html', {'msg': '该数据不存在，无法重置！'})
    if request.method == 'GET':
        forms = AdminResetModelForm(instance=reset_querySet)
        return render(request, 'public-add.html', {'forms': forms, 'title': title})

    forms = AdminResetModelForm(data=request.POST, instance=reset_querySet)
    if forms.is_valid():
        forms.save()
        return HttpResponse("<script>alert('重置成功, 请重新登录'); window.location='/login/';</script>")
    return render(request, 'public-add.html', {'forms': forms, 'title': title})


def admin_show(request, nid):
    """
    显示密码
    :param nid:
    :param request:
    :return:
    """
    # 获取该id对应用户密码
    pwd = models.Admin.objects.filter(id=nid).first().password
    # print(pwd)
    search_dict = {}
    # 获取搜索词
    search_value = request.GET.get('q', '')
    if search_value:
        search_dict['username__contains'] = search_value

    # 获取搜索的值 在数据库中进行查找
    querySet = models.Admin.objects.filter(**search_dict).order_by('-username')

    # 获取分页数据
    admin_object = myPage.pagination(request, querySet, page_size=5)

    context = {
        'querySet': admin_object.pageQuerySet,
        'search_value': search_value,
        'admin_page_html': admin_object.html(),
        'pwd': pwd
    }

    return render(request, 'admin-list.html', context)

# def admin_login(request):
#     """
#     用户登录
#     :param request:
#     :return:
#     """
#
#     if request.method == 'GET':
#         forms = Login()
#
#         return render(request, 'login.html', {'forms': forms})
#
#     # 处理POST的请求
#     forms = Login(data=request.POST)
#     if forms.is_valid():
#         # 获取用户输入的值
#         # print(forms.cleaned_data)
#
#         exist = models.Admin.objects.filter(**forms.cleaned_data).first()
#         if not exist:
#             forms.add_error('password', '用户名或者密码有误!')
#             return render(request, 'login.html', {'forms': forms})
#         # 设置会话
#         request.session['info'] = {'id': exist.id, 'name': exist.username}
#         # 跳转到管理员列表中
#         return HttpResponse("<script>alert('登录成功');window.location='/admin/list/';</script>")
#     return render(request, 'login.html', {'forms': forms})
#
#
# def admin_out(request):
#     """
#     注销用户的cookie信息
#     :param request:
#     :return:
#     """
#     request.session.clear()
#     return redirect('/login/')
