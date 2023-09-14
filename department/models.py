from django.db import models


# Create your models here.
class Departments(models.Model):
    """
    创建一个部门表
    """
    # 表示该表的字段id 默认情况Django会自动创建
    # id = models.BigAutoField(verbose_name='ID', primary_key=True)

    # 部门名称
    depart_name = models.CharField(verbose_name="部门名称", max_length=30)

    # 部门人数
    depart_person = models.IntegerField(verbose_name='部门人数', default=100)

    depart_introduce = models.CharField(verbose_name='部门介绍', max_length=50, null=True, blank=True, default='你好')

    depart_images = models.CharField(verbose_name='部门图片', max_length=255, null=True, blank=True, default='Hello')

    depart_principal = models.CharField(verbose_name='部门负责人', max_length=30, null=True, blank=True, default='明明')

    def __str__(self):
        return self.depart_name


class UserInfo(models.Model):
    """
    创建一个员工信息
    """
    user_name = models.CharField(verbose_name="姓名", max_length=25)
    gender_choices = (
        (0, '女'),
        (1, '男')
    )
    user_gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choices)
    user_age = models.IntegerField(verbose_name="年龄")
    user_address = models.CharField(verbose_name="家庭地址", max_length=30)
    user_email = models.CharField(verbose_name="邮箱", max_length=30)
    # decimal_places 表示小数点保留位数  max_digits 表示最大位数 个十百千万
    user_salary = models.DecimalField(verbose_name="工资", default=0, decimal_places=2, max_digits=8)
    user_entry_time = models.DateTimeField(verbose_name="入职时间")

    # 设置一个外键 受约束的外键
    # to  表示需要关联的表
    # to_field 表示需要关联的字段 列
    # on_delete models.CASCADE 表示级联删除
    depart = models.ForeignKey(verbose_name='部门', to='Departments', to_field='id', on_delete=models.CASCADE)

    # 设置关联表的操作 当删除数据时，关联的字段设置为空
    # depart = models.ForeignKey(to='Departments', to_field='id', null=True, blank=True, on_delete=models.SET_NULL)


class Other(models.Model):
    """
    多条显示
    """
    data = models.IntegerField(verbose_name='变量')
    page = models.IntegerField(verbose_name='页数')


class PrettyNum(models.Model):
    """
    靓号管理
    """
    mobile = models.CharField(verbose_name='手机号', max_length=20)
    price = models.IntegerField(verbose_name='价格', default=0, null=True, blank=True)

    # 级别种子
    level_choices = (
        (0, '未评级'),
        (1, '一星'),
        (2, '二星'),
        (3, '三星'),
        (4, '四星'),
        (5, '五星'),
    )

    level = models.SmallIntegerField(verbose_name='级别', choices=level_choices, default=0)

    # 使用情况
    status_choices = (
        (1, '未使用'),
        (2, '已使用')
    )
    status = models.SmallIntegerField(verbose_name='状态', choices=status_choices, default=1)


class Title(models.Model):
    """
    轮播图
    """
    # 名称
    name = models.CharField(verbose_name='名称', max_length=30)
    # 链接
    url = models.CharField(verbose_name='链接', max_length=255, null=True, blank=True, default='notImages')


class Admin(models.Model):
    """
    创建管理员
    """
    # 姓名
    username = models.CharField(verbose_name='用户名', max_length=255)
    # 密码
    password = models.CharField(verbose_name='密码', max_length=255)

    def __str__(self):
        return self.username


class Device(models.Model):
    """
    创建设备任务
    """
    # 任务标题
    title = models.CharField(verbose_name='标题', max_length=60)
    # 任务详情
    detail = models.TextField(verbose_name='详情')
    # 任务级别
    level_choices = (
        (1, '紧急'),
        (2, '重要'),
        (3, '一般'),
        (4, '延缓'),
    )
    level = models.SmallIntegerField(verbose_name='级别', choices=level_choices)

    # 负责人
    person = models.ForeignKey(verbose_name='负责人', to='Admin', to_field='id', on_delete=models.CASCADE)


class Order(models.Model):
    """
    创建订单表
    """
    # 订单编号
    order_id = models.CharField(verbose_name='订单编号', max_length=100)

    # 订单名称
    order_name = models.CharField(verbose_name='订单名称', max_length=100)

    # 订单价格
    order_price = models.IntegerField(verbose_name='订单价格')

    # 订单状态
    static_choices = (
        (1, '未支付'),
        (2, '已支付'),
    )
    order_static = models.SmallIntegerField(verbose_name='订单状态', choices=static_choices, default=1)

    # 订单负责人
    person = models.ForeignKey(verbose_name='订单负责人', to='Admin', to_field='id', on_delete=models.CASCADE)
