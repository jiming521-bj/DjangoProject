# -*- coding: utf-8 -*-
# @Time     : 2023/9/10 11:33
# @Author   : JiMing
# @File     : index.py
# @SoftWare : PyCharm

from django.shortcuts import render, HttpResponse, redirect
from department.models import Departments, UserInfo, Title
import json
from department.my_forms import Login
from department import models
from department.utils import code
from io import BytesIO


def index_layout(request):
    """
    加载模板文件
    :param request:
    :return:
    """
    images_list = [i for i in range(1, 7)]
    # 获取部门信息的前六位信息
    querySet = Departments.objects.all()[:6]

    image_list_1 = [i for i in range(7, 11)]
    image_list_2 = [i for i in range(11, 14)]
    querySet_1 = Departments.objects.all()[6:10]
    querySet_2 = Departments.objects.all()[10:14]

    user_querySet = UserInfo.objects.all()

    # 获取用户以及对应的薪资
    names = []
    salary = []
    user_salary = UserInfo.objects.values_list('user_name', 'user_salary')
    for query in user_salary:
        names.append(query[0])
        salary.append(int(query[1]))
    # print(user_salary)
    # print(names)
    # print(salary)
    data_set = {
        'names': names,
        'salary': salary
    }
    # 获取轮播图
    url_query_set = Title.objects.all()

    print(url_query_set)

    # print(json.dumps(data_set))
    context = {'querySet': querySet, 'images': images_list, 'querySet_1': querySet_1,
               'querySet_2': querySet_2, 'images_1': image_list_1, 'images_2': image_list_2,
               'user_querySet': user_querySet, 'data': data_set, 'url_set': url_query_set}
    return render(request, 'index.html', context)


# Create your views here.
def index(request):
    """
    响应一个简单的计算器
    :param request:
    :return:
    """
    if request.method == 'POST':
        n1 = request.POST.get('num1')
        n2 = request.POST.get('num2')
        n3 = int(n1) + int(n2)
        return HttpResponse(n3)
    return render(request, 'depart-index.html')


def index_login(request):
    """
    用户登录
    :param request:
    :return:
    """

    if request.method == 'GET':
        forms = Login()

        return render(request, 'login.html', {'forms': forms})

    # 处理POST的请求
    forms = Login(data=request.POST)
    if forms.is_valid():
        # 获取用户输入的值
        # print(forms.cleaned_data)
        # 验证用户输入的验证码
        fromData = forms.cleaned_data
        try:
            session_code = request.session['image_code']
        except KeyError:
            return HttpResponse("<script>alert('验证码超时');window.location='/login';</script>")  # 如果登录页面超时，返回到登录页
        input_code = forms.cleaned_data.pop('code')

        if session_code != input_code:
            forms.add_error('code', '验证码有误!')
            return render(request, 'login.html', {'forms': forms})
        exist = models.Admin.objects.filter(**fromData).first()
        if not exist:
            forms.add_error('password', '用户名或者密码有误!')
            return render(request, 'login.html', {'forms': forms})
        # 设置会话
        request.session['info'] = {'id': exist.id, 'name': exist.username}
        request.session.set_expiry(60 * 60 * 24 * 7)  # 保存时间为7天
        # 跳转到管理员列表中
        return HttpResponse("<script>alert('登录成功');window.location='/';</script>")
    return render(request, 'login.html', {'forms': forms})


def index_out(request):
    """
    注销用户的cookie信息
    :param request:
    :return:
    """
    request.session.clear()
    return HttpResponse("<script>window.alert('注销成功'); window.location='/login/';</script>")


def image_code(request):
    """
    生成随机图片
    :param request:
    :return:
    """
    if request.method == 'GET':
        # 调用pillow函数生成图片
        img, string_img = code.check_code()

        # 将图片的验证码写入到session会话中
        request.session['image_code'] = string_img
        # 设置Session的会话超时 60s
        request.session.set_expiry(60)

        # 写入到内存中
        stream = BytesIO()
        img.save(stream, 'png')

        return HttpResponse(stream.getvalue())
