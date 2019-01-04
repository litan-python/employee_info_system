from django.core.paginator import Paginator
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, redirect, HttpResponse
from acountapp.models import Acount
from operateapp.models import Employee
from datetime import datetime
from acountapp.captcha.image import ImageCaptcha
import random,string

# Create your views here.
#登录页面
def login(request):
    name = request.COOKIES.get("username")
    pwd = request.COOKIES.get("userpwd")
    now = datetime.now()
    if name == None:
        return render(request, "acountapp/login.html", {"time": now})
    else:
        if Acount.objects.filter(username=name.encode('latin-1').decode('utf-8'),userpwd=pwd):
            request.session["login"] = "ok"
            return redirect("acountapp:main")
        return render(request, "acountapp/login.html", {"time": now})


#登录操作，验证是否成功
def login_logic(request):
    name = request.POST.get("name")
    pwd = request.POST.get("pwd")
    if Acount.objects.filter(username=name,userpwd=pwd):
        rsp = redirect("acountapp:main")
        request.session["login"] = "ok"
        rsp.set_cookie("username",name.encode('utf-8').decode('latin-1'),max_age=7*24*60*60)
        rsp.set_cookie("userpwd",pwd,max_age=7*24*60*60)
        return rsp
    else:
        return render(request,"acountapp/login.html",{"error_msg":"账号或密码错误，请重新输入"})

# 获取随机验证码图片
def getCaptcha(request):
    image = ImageCaptcha()  # 为验证码设置字体，无参为默认字体
    code = random.sample(string.ascii_letters + string.digits, 5)  # 设置一个5位的随机码，由字母和数字组成
    # 将验证码已字符串形式存入session
    code = "".join(code)
    request.session["code"] = code
    # 已生成的随机字符串为文本生成一个图片传回前端页面
    data = image.generate(code)
    return HttpResponse(data, "image/png")

#显示注册页面
def regist(request):
    now = datetime.now()
    return render(request, "acountapp/regist.html", {"time":now})

#将注册信息提交到数据库
def regist_logic(request):
    name = request.POST.get("username")
    rname = request.POST.get("name")#获取真实姓名
    pwd = request.POST.get("pwd")
    sex = request.POST.get("sex")
    code = request.POST.get("number")
    if name == "" or rname == "" or pwd == "" or sex == "":
        return HttpResponse("输入不能为空")
    if code.upper() != request.session.get("code").upper():
        return HttpResponse("验证码输入错误，请从新输入")
    try:
        with transaction.atomic():
            Acount.objects.create(username=name,realname=rname,userpwd=pwd,sex=sex)
        return redirect("acountapp:login")
    except:
        return HttpResponse("用户已存在，请直接登录")

#显示登陆成功后的主页面
def main(request):
    # 从数据库获取员工信息列表
    # empList = Employee.objects.all()
    # 获取页数
    number = request.GET.get("num")
    if number == None:
        number = 1
    # 构造分页器对象
    pagtor = Paginator(Employee.objects.all(), per_page=3)
    now = datetime.now()
    return render(request, "acountapp/emplist.html", {"page":pagtor.page(number),"time":now})

# 检查用户名是否合法
def checkname(request):
    username = request.GET.get("name")
    if username == "":
        return HttpResponse("<img src='/static/img/error_3.jpg' width='25px' height='25px'>用户名不能为空")
    if Acount.objects.filter(username=username):
        return HttpResponse("<img src='/static/img/error_3.jpg' width='25px' height='25px'>此用户名已被注册")
    else:
        return HttpResponse("<img src='/static/img/right.jpg' width='25px' height='25px'>此用户名可以使用")

def checkcode(request):
    code = request.GET.get("code")
    code_session = request.session.get("code")
    if code.upper() == code_session.upper():
        return HttpResponse("<img src='/static/img/right.jpg' width='25px' height='25px'>")
    else:
        return HttpResponse("<img src='/static/img/error_3.jpg' width='25px' height='25px'>")

# 将Employee实例对象转化为字典形式，其中将ImageFiled对象转化为字符串对象
def mydefault(employee):
    if isinstance(employee, Employee):
        return {"id":employee.id,"name":employee.name,"salary":employee.salary,"age":employee.age,"headpic":str(employee.headpic)}
#查询函数
def query(request):
    name = request.POST.get("name")
    employeelist = Employee.objects.filter(name__contains=name)
    return JsonResponse(list(employeelist),safe=False,json_dumps_params={"default":mydefault})


