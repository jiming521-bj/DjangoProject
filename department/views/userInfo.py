# -*- coding: utf-8 -*-
# @Time     : 2023/9/10 11:32
# @Author   : JiMing
# @File     : userInfo.py
# @SoftWare : PyCharm
from django.shortcuts import render, redirect, HttpResponse
from department.models import UserInfo, Departments
from department.my_forms import MyModelFrom
from department.utils.myPage import pagination


def user_list(request):
    """
    用户列表
    :param request:
    :return:
    """
    # 获取user表中的所有字段
    querySet = UserInfo.objects.all()

    page_object = pagination(request, querySet, page_size=5)
    # 测试数据是否正确
    # 如果表中有关联数据 使用外键名称获取对应的外键字段 外键字段.外表字段
    # 想要获取Django中ORM模型自定义的关联数据 使用get_自定义数据名_display()
    # for set_value in querySet:
    #     print(set_value.user_name, set_value.get_user_gender_display())
    context = {
        'querySet': page_object.pageQuerySet,
        'page_html': page_object.html()
    }
    return render(request, 'user-list.html', context)


def user_add(request):
    """
    添加用户
    :param request:
    :return:
    """
    if request.method == 'GET':
        # 获取性别和部门id
        content = {
            'choices': UserInfo.gender_choices,
            'departs': Departments.objects.all(),
        }
        return render(request, 'user-add.html', content)

    # POST请求
    method_type = request.POST
    name = method_type.get('name')
    gender = method_type.get('gender')
    age = method_type.get('age')
    address = method_type.get('address')
    email = method_type.get('mail')
    salary = method_type.get('salary')
    entry_time = method_type.get('ctime')
    depart_id = method_type.get('depart')

    # 插入到数据库中
    UserInfo.objects.create(
        user_name=name,
        user_gender=gender,
        user_address=address,
        user_age=age,
        user_email=email,
        user_salary=salary,
        user_entry_time=entry_time,
        depart_id=depart_id
    )
    return HttpResponse("<script>alert('添加成功');window.location='/user/list/';</script>")


def user_model_form_add(request):
    """
    使用ModelForm提交数据
    :param request:
    :return:
    """
    if request.method == 'GET':
        # 实例化ModelForm
        form = MyModelFrom()

        return render(request, 'user-model-form-add.html', {'forms': form})

    # POST 提交
    form = MyModelFrom(request.POST)

    if form.is_valid():
        # 如果数据不为空 直接保存
        form.save()
        return HttpResponse("<script>alert('添加成功');window.location='/user/list/';</script>")
    # 校验失败
    return render(request, 'user-model-form-add.html', {'forms': form})


def user_edit(request, nid):
    """
    编辑用户信息
    :param nid:
    :param request:
    :return:
    """
    # 获取用户信息
    rol_object = UserInfo.objects.filter(id=nid).first()
    if request.method == 'GET':
        # 实例化modelForm
        form = MyModelFrom(instance=rol_object)
        return render(request, 'user-edit.html', {'forms': form})

    # 校验POST数据
    form = MyModelFrom(data=request.POST, instance=rol_object)
    if form.is_valid():
        # 额外添加字段值
        # form.instance.user_sing = 'ke'
        form.save()
        return HttpResponse("<script>alert('修改成功');window.location='/user/list/';</script>")
    # 返回错误信息
    return render(request, 'user-edit.html', {'forms': form})
    # return render(request, 'user-edit.html')


def user_delete(request, did):
    """
    删除用户
    :param did:
    :param request:
    :return:
    """
    # 获取当前删除的用户id
    if request.method == 'GET':
        UserInfo.objects.filter(id=did).delete()
        return redirect('/user/list/')
