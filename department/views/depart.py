# -*- coding: utf-8 -*-
# @Time     : 2023/9/10 11:32
# @Author   : JiMing
# @File     : depart.py
# @SoftWare : PyCharm
from django.shortcuts import render, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import math
from department import models


# @csrf_exempt  解除csrf_token的验证
def depart_list(request):
    """
    部门列表
    :param request:
    :return:
    """

    # 获取数据库中部门表中的信息
    # query_set = serializers.serialize('json', models.Departments.objects.all())
    # print(json.dumps(query_set))
    # with open('w.txt', 'w', encoding='utf-8') as file:
    #     file.writelines(json.dumps(query_set))
    if request.method == 'GET':
        # 获取全部部门信息
        query_set = models.Departments.objects.all().order_by('id')
        # 统计部门个数
        cnt = models.Departments.objects.all().count()

    else:
        query_value = request.POST['search_value']
        # 获取指定部门信息
        query_set = models.Departments.objects.filter(depart_name__icontains=query_value).order_by('id')
        # 统计指定部门个数
        cnt = models.Departments.objects.filter(depart_name__icontains=query_value).count()

        if cnt == 0:
            return HttpResponse(
                """
               <script>
               alert('找不到对应的部门');window.history.go(-1);
                window.onload = function(){
                    let isPageHide = false;
                    window.addEventListener('pageshow', function (){
                        if (isPageHide){
                            window.location.reload();
                        }
                    });
                    window.addEventListener('pagehide', function (){
                        isPageHide = true;
                    })
                }
                </script>
                """
            )

    # 设置页码数
    page_list = [i for i in range(1, 10000)]

    # 每页展示的数据值
    page_value = 5
    cnt_value = math.ceil(cnt / page_value)

    # 获取当前页码值
    page_number = request.GET.get('page')
    if page_number is None:
        page_number = 1
    else:
        page_number = int(page_number)

    # 将表中的数据和显示数绑定
    paginator = Paginator(query_set, page_value)  # per_page为每页显示的数据量
    try:
        page_data = paginator.page(page_number)  # page_number为要获取的页码
    except PageNotAnInteger:
        page_data = paginator.page(1)  # 如果不是整数，则默认获取第一页的数据
    except EmptyPage:
        page_data = paginator.page(paginator.num_pages)  # 如果超出范围，则获取最后一页的数据
    # 响应数据至前端

    return render(request, 'depart-list.html',
                  {'dataSet': query_set, 'page_data': page_data,
                   'cnt_value': page_list[0:cnt_value],
                   'page_number': page_number})


def depart_add(request):
    """
    添加部门
    :param request:
    :return:
    """
    # 获取所有部门名称
    title_list = []
    query_set = models.Departments.objects.all()
    for obj in query_set:
        title_list.append(obj.depart_name)

    if request.method == 'GET':
        return render(request, 'depart-add.html')

    # 获取数据表 向表中插入数据
    title = request.POST.get('depart_name')
    # print(title)
    # print(type(title))
    # 判断输入的是否已经存在的 如果存在不允许添加 否则添加
    if title in title_list:
        return HttpResponse("<script>alert('部门已存在');window.location='/depart/add/';</script>")
    # 判断输入的是否为空
    if title == '':
        return HttpResponse("<script>alert('部门名称不能为空');window.location='/depart/add/';</script>")
    models.Departments.objects.create(depart_name=title)
    # 重定向到员工信息表中
    # return redirect('/depart/list/')
    return HttpResponse("<script>alert('添加成功');window.location='/depart/list/?page=1';</script>")


def depart_delete(request):
    """
    删除部门信息
    :param request:
    :return:
    """
    # 获取所有id
    id_values = []
    query_set = models.Departments.objects.all()
    for ids in query_set:
        id_values.append(ids.id)

    # 获取要删除的部门id
    nid = request.GET.get('nid')
    try:
        nid = eval(nid)
        if int(nid) not in id_values:
            return HttpResponse("<script>alert('不存在该索引值的部门id');window.location='/depart/list/?page=1';</script>")
    except NameError:
        return HttpResponse("<script>alert('删除失败!请检查参数');window.location='/depart/list/?page=1';</script>")
    else:
        # 跳转到部门信息列表页
        models.Departments.objects.filter(id=nid).delete()
        return HttpResponse("<script>window.location='/depart/list/?page=1';</script>")


def show_list(request):
    """
    多页显示数据
    :param request:
    :return:
    """
    # 计算存储数据和 计算最后一页页面
    count = models.Departments.objects.all().count()

    # 当count=10 、 20 、30。。时，计算最后一页，10/10+1就等于2了，这个bug
    # 所以当count=10。。。， 进行count - 1，int（count/10）+1 = 1，这样最后一页计算就对了
    for i in range(0, 1001, 10):
        if count == i:
            count = count - 1

    end = int(count / 10) + 1

    # 获取数据库上的变量和页数，显示数据条和初始页数
    sql = models.Other.objects.filter(id=1).first()
    sqldata = sql.data
    sqlpage = sql.page

    if request.method == "GET":
        data_list = models.Departments.objects.all()[0:10]
        models.Other.objects.filter(id=1).update(data=10, page=1)
        return render(request, 'show-page.html', {'data_list': data_list, 'count': count, 'page': 1, 'end': end})

    paging = request.GET.get("paging")

    if paging == 'nx':
        if sqldata != end * 10:
            sqldata = sqldata + 10
            data_list = models.Departments.objects.all()[sqldata - 10:sqldata]
            sqlpage = sqlpage + 1
            models.Other.objects.filter(id=1).update(data=sqldata, page=sqlpage)
            return render(request, 'show-page.html',
                          {'data_list': data_list, 'count': count, 'page': sqlpage, 'end': end, 'data': sqldata})
        else:
            data_list = models.Departments.objects.all()[end * 10 - 10:end * 10]
            return render(request, 'show-page.html', {'data_list': data_list, 'count': count, 'page': end, 'end': end})
    elif paging == 'pr':
        if sqldata != 10:
            sqldata = sqldata - 10
            data_list = models.Departments.objects.all()[sqldata - 10:sqldata]
            sqlpage = sqlpage - 1
            models.Other.objects.filter(id=1).update(data=sqldata, page=sqlpage)
            return render(request, 'show-page.html',
                          {'data_list': data_list, 'count': count, 'page': sqlpage, 'end': end, 'data': sqldata})
        else:
            data_list = models.Departments.objects.all()[0:10]
            return render(request, 'show-page.html',
                          {'data_list': data_list, 'count': count, 'page': sqlpage, 'end': end, 'data': sqldata})
    elif paging == 'first':
        models.Other.objects.filter(id=1).update(data=10, page=1)
        data_list = models.Departments.objects.all()[0:10]
        return render(request, 'show-page.html', {'data_list': data_list, 'count': count, 'page': 1, 'end': end})
    elif paging == 'end':
        models.Other.objects.filter(id=1).update(data=end * 10, page=end)
        data_list = models.Departments.objects.all()[end * 10 - 10:end * 10]
        return render(request, 'show-page.html', {'data_list': data_list, 'count': count, 'page': end, 'end': end})


def depart_update(request):
    """
    修改部门信息
    :param request:
    :return:
    """
    uid = request.GET.get('uid')
    # 发送GET请求响应的内容
    if request.method == 'GET':
        query_set = models.Departments.objects.filter(id=uid)
        return render(request, 'depart-update.html', {'query_set': query_set})

    # 获取所有部门名称
    title_list = []
    data_set = models.Departments.objects.all()
    for obj in data_set:
        title_list.append(obj.depart_name)
    # 发送POST请求响应的内容
    # 获取数据表 向表中插入数据
    title = request.POST.get('depart_name')
    # print(title)
    # print(uid)
    # 判断输入的是否已经存在的 如果存在不允许添加 否则添加
    if title in title_list:
        return HttpResponse("<script>alert('部门已存在');window.history.go(-1);</script>")

    # 修改数据
    models.Departments.objects.filter(id=uid).update(
        depart_name=title
    )
    # 重定向到员工信息表中
    # return redirect('/depart/list/')
    return HttpResponse("<script>alert('修改成功');window.location='/depart/list/?page=1';</script>")
