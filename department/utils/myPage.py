# -*- coding: utf-8 -*-
# @Time     : 2023/9/9 16:55
# @Author   : JiMing
# @File     : myPage.py
# @SoftWare : PyCharm
from django.utils.safestring import mark_safe
import copy
from django.http.request import QueryDict

"""
返回的数据pageQuerySet
前端页码的配置存在html()中
前端显示页码配置的条件
    <ul class="pagination">
        {{ page_html }}
    </ul>
"""


class pagination(object):
    """
    实现分页功能的组件
    """

    def __init__(self, request, querySet, page_size=10, page_param='page', plus=3):
        """

        :param request: 请求的对象
        :param querySet: 获取数据库的结果对象
        :param page_size: 页码条数
        :param page_param: 页面
        :param plus: 页码的范围
        """
        # 获取对象的拷贝
        page_copy_object = copy.deepcopy(request.GET)
        # print(type(page_copy_object))   # QueryDict对象
        page_copy_object._mutable = True  # 允许添加属性拼接

        self.page_copy_object = page_copy_object

        page = request.GET.get(page_param, '1')
        if page.isdecimal():
            page = int(page)
        else:
            page = 1
        # 初始化第一页
        self.page = page

        # 参数对象
        self.page_param = page_param

        # 初始化页码
        self.page_size = page_size

        # 获取起始值显示条数和终止值
        self.start = (self.page - 1) * self.page_size
        self.end = self.page * self.page_size

        # 每页的数据结果
        self.pageQuerySet = querySet[self.start: self.end]
        self.pageCnt = querySet.count()
        total_page_count, div = divmod(self.pageCnt, self.page_size)
        if div:
            total_page_count += 1
        # 获取总页码
        self.total_value = total_page_count

        # 获取页码范围
        self.plus = plus

    def html(self):
        # 生成页码数
        page_list = []

        # 如果页面没有满足显示的最大上限
        if self.total_value <= 2 * self.plus + 1:
            page_start = 1
            page_end = self.total_value
        else:
            # 数据量大于上限值
            # 当前值小于5页
            if self.page <= self.plus:
                page_start = 1
                page_end = 2 * self.plus + 1
            else:
                # 当前值大于5
                if (self.page + self.plus) > self.total_value:
                    page_start = self.total_value - 2 * self.plus
                    page_end = self.total_value
                else:
                    page_start = self.page - self.plus
                    page_end = self.page + self.plus
        # page_copy_object.setlist('xx', [11])
        # print(page_copy_object.urlencoded())

        self.page_copy_object.setlist(self.page_param, [1])
        # print(self.page_copy_object.urlencode())
        # 设置首页
        first = f"<li><a href='?{self.page_copy_object.urlencode()}'>首页</a></li>"
        # 设置上一页和下一页
        # 上一页
        if self.page > 1:
            self.page_copy_object.setlist(self.page_param, [self.page - 1])
            prev = f"<li><a href='?{self.page_copy_object.urlencode()}'>上一页</a></li>"
        else:
            self.page_copy_object.setlist(self.page_param, [self.page])
            prev = f"<li><a href='?{self.page_copy_object.urlencode()}'>上一页</a></li>"

        page_list.append(first)
        page_list.append(prev)

        for i in range(page_start, page_end + 1):
            self.page_copy_object.setlist(self.page_param, [i])
            if self.page == i:
                ele = f"<li class='active'><a href='?{self.page_copy_object.urlencode()}'>{i}</a></li>"
            else:
                ele = f"<li><a href='?{self.page_copy_object.urlencode()}'>{i}</a></li>"
            page_list.append(ele)
        # print(page_list)
        # 下一页
        if self.page < self.total_value:
            self.page_copy_object.setlist(self.page_param, [self.page + 1])
            nex = f"<li><a href='?{self.page_copy_object.urlencode()}'>下一页</a></li>"
        else:
            self.page_copy_object.setlist(self.page_param, [self.total_value])
            nex = f"<li><a href='?{self.page_copy_object.urlencode()}'>下一页</a></li>"
        page_list.append(nex)
        # 设置尾页
        self.page_copy_object.setlist(self.page_param, [self.total_value])
        last = f"<li><a href='?{self.page_copy_object.urlencode()}'>尾页</a></li>"
        page_list.append(last)

        search_index = """
           <li style="float: left;">
               <form action="" method="get">
                   <div class="input-group" style="width: 150px;">
                       <input type="text" class="form-control" placeholder="页数" name="page">
                       <span class="input-group-btn"><button class="btn btn-default" type="submit">跳转</button></span>
                   </div>
               </form>
           </li>
           """
        page_list.append(search_index)
        pages = mark_safe("".join(page_list))  # 将每一个链接拼接 使用mark_safe对链接安全验证

        return pages
