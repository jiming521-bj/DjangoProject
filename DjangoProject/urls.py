"""
URL configuration for DjangoProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path
from department.views import depart, index, prettyNum, userInfo, admin, device, order, charts,upload

urlpatterns = [
    # path('admin/', admin.site.urls),
    # path('', views.main),
    # path('index/', views.index),
    # path('my-site/', views.my_site),
    # path('my-request/', views.my_request_response),
    # path('login/', views.login),
    # path('orm/', views.orm),
    # path('user/list/', views.user_list),
    # path('user/add/', views.user_add),
    # path('user/delete/', views.user_delete),
    # path('user/update/', views.user_update),

    # 部门项目路由配置
    path('', index.index_layout),
    # 参数传递 <int:nid>
    path('depart/list/', depart.depart_list),  # 部门列表
    path('depart/add/', depart.depart_add),  # 添加部门
    path('depart/delete/', depart.depart_delete),  # 删除部门
    # path('depart/list/', views.show_list),   # 多条显示部门信息
    path('depart/update/', depart.depart_update),  # 修改部门信息
    path('depart/index/', index.index),  # 测试页面

    # 用户项目
    path('user/list/', userInfo.user_list),  # 用户列表
    path('user/add/', userInfo.user_add),  # 添加用户
    path('user/model/form/add/', userInfo.user_model_form_add),  # 使用ModelForm添加用户
    path('user/<int:nid>/edit/', userInfo.user_edit),  # 编辑用户
    path('user/<int:did>/delete/', userInfo.user_delete),  # 删除用户

    # 靓号管理
    path('pretty/list/', prettyNum.pretty_list),  # 靓号列表
    path('pretty/add/', prettyNum.pretty_add),  # 靓号的添加
    path('pretty/<int:nid>/edit/', prettyNum.pretty_edit),  # 编辑靓号
    path('pretty/<int:did>/delete/', prettyNum.pretty_delete),  # 删除靓号

    # 管理员管理
    path('admin/list/', admin.admin_list),
    path('admin/add/', admin.admin_add),
    path('admin/<int:nid>/edit/', admin.admin_edit),
    path('admin/<int:nid>/delete/', admin.admin_delete),
    path('admin/<int:nid>/reset/', admin.admin_reset),
    # path('admin/<int:nid>/show/', admin.admin_show),
    # 用户登录
    # path('login/', admin.admin_login),
    # path('loginout/', admin.admin_out),
    path('login/', index.index_login),
    path('loginout/', index.index_out),
    path('image/code/', index.image_code),

    # 设备管理
    path('device/list/', device.device_list),
    path('device/ajax/', device.device_ajax),
    path('device/add/', device.device_add),
    path('device/<int:nid>/delete/', device.device_delete),
    path('device/muilt/', device.device_muilt),

    # 订单管理
    path('order/list/', order.order_list),
    path('order/add/', order.order_add),
    path('order/detail/', order.order_detail),
    path('order/edit/', order.order_edit),
    path('order/delete/', order.order_delete),

    # ECharts图表
    path('echarts/list/', charts.charts_list),
    path('charts/line/', charts.charts_line),
    path('charts/bar/', charts.charts_bar),
    path('charts/pei/', charts.charts_pei),

    # 文件上传
    path('upload/list/', upload.upload_list),
    path('upload/value/', upload.upload_value),
]
