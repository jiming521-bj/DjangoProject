# -*- coding: utf-8 -*-
# @Time     : 2023/9/14 11:23
# @Author   : JiMing
# @File     : charts.py
# @SoftWare : PyCharm

from django.shortcuts import render, HttpResponse, redirect
from department import models
import json


def charts_list(request):
    """
    Echarts图表
    :param request:
    :return:
    """
    return render(request, 'echarts-list.html')


def charts_line(request):
    """
    设置折线图数据
    :param request:
    :return:
    """
    if request.method == 'GET':

        # 获取手机号的前6条数据
        query_six_Set = models.PrettyNum.objects.values('mobile', 'price').all()[0:6]
        print(query_six_Set)
        phone_list = []
        price_list = []
        for set_value in query_six_Set:
            phone_list.append(set_value['mobile'])
            price_list.append(set_value['price'])

        title = '靓号价格统计折线图'
        x_axis_data = phone_list
        series_data = price_list
        context = {
            'title': title,
            'x_axis': x_axis_data,
            'series': series_data,
        }
        return HttpResponse(json.dumps(context))


def charts_bar(request):
    """
    获取柱状图信息
    :param request:
    :return:
    """
    y_axis = []
    series_data = []
    query_ten_Set = models.UserInfo.objects.values('user_name', 'user_salary').all()[:10]
    for set_value in query_ten_Set:
        y_axis.append(set_value['user_name'])
        series_data.append({'value': int(set_value['user_salary']), 'label': 'labelRight'})
    context = {
        'title': '工资柱状图',
        'y_axis': y_axis,
        'series': series_data,

    }
    return HttpResponse(json.dumps(context))


def charts_pei(request):
    """
    获取所有部门的部门名称和部门负责人展示到饼图中
    :param request:
    :return:
    """
    series_data = []
    querySixSet = models.Departments.objects.values('depart_person', 'depart_name').all()[:6]
    for set_value in querySixSet:
        print(set_value)
        series_data.append({"value": set_value['depart_person'], "name": set_value['depart_name']})
    context = {
        'title': '部门分布情况',
        'series': series_data,
    }
    return HttpResponse(json.dumps(context))
