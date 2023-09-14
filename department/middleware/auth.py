# -*- coding: utf-8 -*-
# @Time     : 2023/9/11 20:44
# @Author   : JiMing
# @File     : auth.py
# @SoftWare : PyCharm
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse, redirect


class Auth(MiddlewareMixin):
    def process_request(self, request):
        """
        模拟中间件的请求
        :return:
        """
        # 如果有返回值 返回请求对象HttpResponse render redirect
        # 如果没有返回值 None 继续下一个中间件走

        print('我是第一个中间件请求')
        return HttpResponse("这是一场没有尽头的旅途")

    def process_response(self, request, response):
        """
        模拟中间件的响应
        :return:
        """
        print('我是第一个中间件的响应')
        return response


class Auth1(MiddlewareMixin):
    def process_request(self, request):
        """
        模拟中间件的请求
        :return:
        """
        print('我是第二个中间件请求')

    def process_response(self, request, response):
        """
        模拟中间件的响应
        :return:
        """
        print('我是第二个中间件的响应')
        return response


class AuthMiddleWare(MiddlewareMixin):
    """
    验证用户是否登录
    """
    def process_request(self, request):
        """
        验证用户登录状态
        :param request:
        :return:
        """
        # 获取不需要登录的用户界面
        other_login_path = request.path_info
        if other_login_path in ['/login/', '/', '/image/code/']:
            return

        # 验证 如果登录过
        info_dict = request.session.get('info')
        if info_dict:
            return
        return HttpResponse("<script>alert('请先登录后操作');window.location='/';</script>")
