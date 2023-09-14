# -*- coding: utf-8 -*-
# @Time     : 2023/9/10 11:32
# @Author   : JiMing
# @File     : prettyNum.py
# @SoftWare : PyCharm
from django.shortcuts import render, redirect, HttpResponse
from department.my_forms import MyPrettyModelForm, MyPrettyEditModelForm
from department.utils.myPage import pagination
from department import models


def pretty_list(request):
    """
    靓号列表 版本2
    :param request:
    :return:
    """
    # 临时添加数据
    # for i in range(100):
    #     models.PrettyNum.objects.create(mobile=18386735185, price=500, level=1, status=1)

    search_dict = {}
    # 获取搜索词
    search_value = request.GET.get('q', '')
    if search_value:
        search_dict['mobile__contains'] = search_value

    # 获取搜索的值 在数据库中进行查找
    querySet = models.PrettyNum.objects.filter(**search_dict).order_by('-level', '-price')

    # 分页对象
    page_object = pagination(request, querySet, page_size=5)

    # 页面对象
    html = page_object.html()

    context = {'querySet': page_object.pageQuerySet,
               'search_value': search_value,
               'pages': html}
    # 返回结果对象
    return render(request, 'pretty-list.html', context)


def pretty_add(request):
    """
    添加靓号
    :param request:
    :return:
    """
    # get方式去请求的展示页面
    if request.method == 'GET':
        pretty_forms = MyPrettyModelForm()
        return render(request, 'pretty-add.html', {'forms': pretty_forms})
    # post方式请求的提交数据

    pretty_forms = MyPrettyModelForm(data=request.POST)
    if pretty_forms.is_valid():
        # 保存数据
        # print(pretty_forms.cleaned_data)
        pretty_forms.save()
        return HttpResponse("<script>alert('添加成功');window.location='/pretty/list/'</script>")
    return render(request, 'pretty-add.html', {'forms': pretty_forms})


def pretty_edit(request, nid):
    """
    靓号的编辑
    :param request:
    :param nid:
    :return:
    """
    # 获取nid对应的编辑数据对象
    pretty_query_set = models.PrettyNum.objects.filter(id=nid).first()
    if request.method == 'GET':
        pretty_forms = MyPrettyEditModelForm(instance=pretty_query_set)
        return render(request, 'pretty-edit.html', {'forms': pretty_forms})

    # POST请求
    pretty_forms = MyPrettyEditModelForm(data=request.POST, instance=pretty_query_set)
    if pretty_forms.is_valid():
        # 保存数据
        pretty_forms.save()
        return HttpResponse("<script>alert('修改成功');window.location='/pretty/list/';</script>")
    return render(request, 'pretty-edit.html', {'forms': pretty_forms})


def pretty_delete(request, did):
    """
    删除靓号
    :param request:
    :param did:
    :return:
    """
    if request.method == 'GET':
        models.PrettyNum.objects.filter(id=did).delete()

        # 重定向到pretty-list.html中
        return redirect('/pretty/list/')

# def pretty_list(request):
#     """
#     靓号列表
#     :param request:
#     :return:
#     """
#     # 获取所有的对象 然后展示到靓号列表中
#     # -表示倒序 级别高的在最上面 desc降序   ACS升序
#     if request.method == 'GET':
#         querySet = models.PrettyNum.objects.all().order_by('-level', '-price')
#         return render(request, 'pretty-list.html', {'querySet': querySet})
#
#     # 获取搜索值
#     value = request.POST.get('search_value')
#     querySet = models.PrettyNum.objects.filter(mobile__contains=value).order_by('-level', '-price')
#     # print(querySet)
#
#     if len(querySet) == 0:
#         return HttpResponse('<script>alert("没有找到对应的数据");window.location="/pretty/list/";</script>')
#     return render(request, 'pretty-list.html', {'querySet': querySet})
