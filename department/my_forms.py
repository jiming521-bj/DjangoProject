# -*- coding: utf-8 -*-
# @Time     : 2023/9/8 12:07
# @Author   : JiMing
# @File     : my_forms.py
# @SoftWare : PyCharm
from django import forms
from department import models
from django.core.validators import RegexValidator
from django.core.validators import ValidationError
from department.utils.bootstrap import Bootstrap
from department.utils.encryption import md5


class MyModelFrom(Bootstrap):
    # 重定义user_name字段的属性值
    user_name = forms.CharField(min_length=3, label='姓名')
    user_entry_time = forms.DateTimeField(widget=forms.DateTimeInput, label="入职日期")

    class Meta:
        model = models.UserInfo
        fields = ['user_name', 'user_gender', 'user_age', 'user_address', 'user_email', 'user_entry_time',
                  'user_salary', 'depart']

        # 手动添加
        # widgets = {
        #     "user_name": forms.TextInput(attrs=({'class': 'form-control'}))
        # }
        widgets = {
            'user_entry_time': forms.DateTimeInput(attrs=({'class': 'form-control'}))
        }


class MyPrettyModelForm(Bootstrap):
    """
    靓号管理的 ModelForm
    """

    # mobile = forms.CharField(max_length=11, label='手机号')

    # 验证手机号 方式一
    # mobile = forms.CharField(label='手机号',
    #                          validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误'), ], )

    class Meta:
        model = models.PrettyNum
        # fields = ['mobile', 'price', 'level', 'status']
        fields = "__all__"  # 表示包含所有字段
        # exclude = ['mobile']  # 表示不包含的字段
        error_messages = {
            'mobile': {
                'required': '请提供手机号！',
                'max_length': '手机号不能超过11位！'
            },
            'price': {
                'required': '请提供价格！',
                'invalid': '您提供的价格无效！'
            }
        }

    # 验证手机号是否存在重复
    def clean_mobile(self):
        """
        获取数据中的手机号与字段的手机号比较
        :return:
        """
        # 数据中的手机列表
        phone_list = []

        # 获取数据中所有电话号码
        m_query_set = models.PrettyNum.objects.values('mobile')
        # 获取数据库中该靓号的个数
        m_query_set_cnt = models.PrettyNum.objects.filter(mobile=self.cleaned_data.get('mobile')).count()

        for i in m_query_set:
            phone_list.append(i.get('mobile', 0))
        # print(phone_list)
        # print(self.cleaned_data.get('mobile'))

        # 获取文本框中用户输入的数据
        input_mobile = self.cleaned_data.get('mobile')

        # 判断手机格式 方式二
        if len(input_mobile) != 11:
            raise ValidationError('手机格式有误')
        else:
            if input_mobile in phone_list:
                raise ValidationError('手机号已被注册')
            return input_mobile

        # if input_mobile in phone_list:
        #     self.add_error('mobile', '该手机号已被注册')
        # else:
        #     return input_mobile

    # 验证价格的有效性
    def clean_price(self):
        """
        获取用户输入的价格进行验证 如果是小于0的提示错误
        :return:
        """

        price = self.cleaned_data.get('price')
        if price is None:
            self.add_error('price', '请提供价格！')
        else:
            if price < 0:
                self.add_error('price', '您提供的价格无效！')
            else:
                return price


class MyPrettyEditModelForm(Bootstrap):
    # 修改的时候 让手机号不能编辑
    # mobile = forms.CharField(disabled=True, label='手机号')

    class Meta:
        model = models.PrettyNum
        # 包含所有字段
        fields = '__all__'

    def clean_mobile(self):
        # 获取编辑的id
        index = self.instance.pk
        text = self.cleaned_data.get('mobile')
        # 排查自己以外的是不是存在本身
        bool_value = models.PrettyNum.objects.exclude(id=index).filter(mobile=text).exists()
        if bool_value:
            raise ValidationError('手机号已经存在')
        return text

    def clean_price(self):
        """
        验证价格
        :return:
        """
        price_input = self.cleaned_data.get('price')
        if price_input < 0:
            raise ValidationError('价格不能小于0')
        else:
            return price_input


class AdminModelForm(Bootstrap):
    """
    添加管理员
    """
    # 添加一个字段 表示重复验证密码
    repeat_password = forms.CharField(label='确认密码',
                                      widget=forms.PasswordInput(render_value=True), )

    class Meta:
        model = models.Admin
        fields = ['username', 'password', 'repeat_password']

        widgets = {
            # render_value 属性为True表示允许密码保留
            'password': forms.PasswordInput(render_value=True),
        }

    # 验证密码
    def clean_repeat_password(self):
        """
        验证密码是否一致
        :return:
        """
        # 获取第一输入的密码
        first_pwd = self.cleaned_data.get('password')
        # 获取第二次输入的密码
        last_pwd = self.cleaned_data.get('repeat_password')

        if first_pwd != md5(last_pwd):
            raise ValidationError("输入的密码不一致")

        return first_pwd

    # 验证姓名
    def clean_username(self):
        """
        验证姓名是否重复注册过
        :return:
        """
        name = self.cleaned_data.get('username')
        sql_data_user = models.Admin.objects.filter(username=name).exists()
        if sql_data_user:
            raise ValidationError("用户名已经注册过")
        return name

    # 将密码加密保存到数据库中
    def clean_password(self):
        """
        对密码加密保存
        :return:
        """
        pwd = md5(self.cleaned_data.get('password'))

        return pwd


class AdminEditModelForm(Bootstrap):
    """
    修改管理员用户名
    """

    class Meta:
        model = models.Admin
        fields = ['username']

    def clean_username(self):
        """
        验证用户名
        :return:
        """
        # 获取用户文本框中的值
        name = self.cleaned_data.get('username')
        # 获取修改用户的id
        nid = self.instance.pk
        if models.Admin.objects.exclude(id=nid).filter(username=name).exists():
            raise ValidationError('该用户名已经存在，换一个吧!')

        return self.cleaned_data.get('username')


class AdminResetModelForm(Bootstrap):
    """
    重置密码
    """
    # 添加一个字段 表示重复验证密码
    repeat_password = forms.CharField(label='确认密码', widget=forms.PasswordInput(render_value=True))

    class Meta:
        model = models.Admin
        fields = ['password', 'repeat_password']

        widgets = {
            'password': forms.PasswordInput()
        }

    # 将密码加密保存到数据库中
    def clean_password(self):
        """
        对密码加密保存
        :return:
        """
        pwd = md5(self.cleaned_data.get('password'))

        # 判断当前的密码是否是原密码
        nid = self.instance.pk
        exist = models.Admin.objects.filter(id=nid, password=pwd).exists()
        if exist:
            raise ValidationError('当前密码不能和原始密码一致')
        return pwd

    # 验证密码
    def clean_repeat_password(self):
        """
        验证密码是否一致
        :return:
        """
        # 获取第一输入的密码
        first_pwd = self.cleaned_data.get('password')
        # 获取第二次输入的密码
        last_pwd = self.cleaned_data.get('repeat_password')

        if first_pwd != md5(last_pwd):
            raise ValidationError("输入的密码不一致")

        return first_pwd


class Login(forms.Form):
    """
    设置登录页面
    """
    username = forms.CharField(label='用户名',
                               widget=forms.TextInput(attrs={'class': 'form-control'}),
                               required=True)
    password = forms.CharField(label='密&nbsp;&nbsp;&nbsp; 码',
                               widget=forms.PasswordInput(render_value=True, attrs={'class': 'form-control'}),
                               required=True)
    code = forms.CharField(label='验证码',
                           widget=forms.TextInput(attrs={'class': 'form-control'}),
                           required=True)

    def clean_password(self):
        pwd = self.cleaned_data.get('password')

        return md5(pwd)


class Device_List(Bootstrap):
    """
    设置任务
    """

    class Meta:
        model = models.Device
        fields = ['title', 'detail', 'level', 'person']

    def clean_title(self):
        """
        验证任务标题
        :return:
        """
        til = self.cleaned_data.get('title')
        print(til)
        print(models.Device.objects.filter(title=til).exists())
        if models.Device.objects.filter(title=til).exists():
            # self.add_error('title', '该数据已经存在')
            raise ValidationError("该任务已经存在")
        return til


class OrderModelForm(Bootstrap):
    """
    订单管理的ModelForm
    """

    class Meta:
        model = models.Order
        # fields = "__all__"

        exclude = ['order_id', 'person']

        error_messages = {
            'order_name': {
                'required': '请提供订单名称！',
            },
            'order_price': {
                'required': '请提供价格！',
            },
            'order_static': {
                'required': '请选择状态！'
            },
            'person': {
                'required': '请提供负责人姓名！'
            }
        }

    def clean_order_price(self):
        """
        校验价格的有效性
        :return:
        """
        price = self.cleaned_data.get('order_price')

        if price < 0:
            raise ValidationError('价格不能小于0！')
        return price
