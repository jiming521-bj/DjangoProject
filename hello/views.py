from django.shortcuts import render, HttpResponse, redirect
from hello.models import userInfo, department


# Create your views here.

def main(request):
    return HttpResponse("main")


def index(request):
    # 响应数据 回传到浏览器中
    return HttpResponse("你的名字")


def my_site(request):
    # 返回主页信息
    html = "这是一个简单的页面"

    return render(request, 'index.html', {'html': html})


def my_request_response(request):
    """
    测试请求和响应
    :param request:
    :return:
    """
    # 获取浏览器使用那种方式请求服务器
    request_method = request.method

    # 获取请求的参数 GET请求方式
    request_param_get = request.GET

    # 获取请求的参数 POST请求方式
    request_param_post = request.POST

    request_dict = {
        'r_method': request_method,
        'r_param_get': request_param_get,
        'r_param_post': request_param_post,
        'name': 'ming',
    }
    # HttpResponse 是将字符串形式返回给用户的浏览器
    # return HttpResponse("这是服务器返回给用户浏览器中的数据")

    # render是将页面渲染后 以html字符返回给用户浏览器
    return render(request, 'request.html', {'value': request_dict})


def login(request):
    """
    模拟简单的用户登录
    :param request:
    :return:
    """
    # 如果用户使用的是GET方式请求 返回登录界面
    if request.method == 'GET':
        return render(request, 'login.html')

    # 获取POST请求的body数据
    name = request.POST.get('user')
    password = request.POST.get('password')

    # print(name, password)
    # 简单的验证数据
    if name == 'admin' and password == 'ming':
        # return redirect('https://www.baidu.com')  # 重定向到百度首页
        return HttpResponse("<script>alert('登录成功');</script>")
    else:
        return render(request, 'login.html', {'error_msg': "登录失败"})


def orm(request):
    """
    测试ORM模块
    :param request:
    :return:
    """
    #  插入数据 向department表中添加三条数据
    # department.objects.create(title="研发部")
    # department.objects.create(title="组织部")
    # department.objects.create(title="策划部")

    # 插入数据 向userInfo表中添加五条数据
    # names = ['ming', 'chen', 'wan', 'li', 'guo', 'wu']
    # ages = [20, 21, 34, 44, 20, 18]
    # for i in range(6):
    #     userInfo.objects.create(
    #         name=names[i],
    #         password='root',
    #         age=ages[i],
    #         size=1048,
    #         data="这是一场没有尽头的旅途"
    #     )

    # 删除数据  存在删除数据 不存在不会删除
    # department.objects.filter(id=16).delete()
    # userInfo.objects.filter(id=1).delete()
    # 删除全部数据
    # department.objects.all().delete()

    # 更新数据
    # department.objects.filter(id=17).update(title="科技部")
    # 更新所有数据
    # userInfo.objects.all().update(age=100)

    # 获取数据  得到都是以行的形式获取的（对象）
    # data_list = department.objects.all()
    # for data in data_list:
    #     print(data.title)

    # 获取第一行数据
    try:
        user_data_list = userInfo.objects.filter(id=2).first()
        print(user_data_list.id, user_data_list.name, user_data_list.data)
    except AttributeError as e:
        raise e
    else:
        print("执行完成")

    return HttpResponse("成功")


def user_list(request):
    """
    用户信息渲染模板
    :param request:
    :return:
    """
    # 获取所有userInfo中的信息
    data_list = userInfo.objects.all()

    return render(request, 'user-list.html', {'data_list': data_list})


def user_add(request):
    """
    添加用户
    :param request:
    :return:
    """
    if request.method == "GET":
        return render(request, 'user-add.html')

    # 返回数据
    name = request.POST.get('username')
    pwd = request.POST.get('password')
    age = request.POST.get('age')
    size = request.POST.get('size')
    data_set = request.POST.get('data')

    # print(name, pwd, age, size, data_set)
    userInfo.objects.create(name=name, password=pwd, age=age, size=size, data=data_set)
    # return HttpResponse("<script>alert('添加成功');</script>")
    return redirect('/user/list')


def user_delete(request):
    """
    删除数据
    :param request:
    :return:
    """
    nid = request.GET.get('id')
    userInfo.objects.filter(id=nid).delete()
    return redirect('/user/list')


def user_update(request):
    """
    用户信息更新
    :param request:
    :return:
    """
    uid = request.GET.get('id')
    if request.method == 'GET':
        data_set = userInfo.objects.filter(id=uid).first()
        return render(request, 'user-update.html', {'data_set': data_set})

    # 返回数据
    name = request.POST.get('username')
    pwd = request.POST.get('password')
    age = request.POST.get('age')
    size = request.POST.get('size')
    data_set = request.POST.get('data')
    userInfo.objects.filter(id=uid).update(
        name=name,
        password=pwd,
        age=age,
        size=size,
        data=data_set
    )
    return redirect('/user/list')
