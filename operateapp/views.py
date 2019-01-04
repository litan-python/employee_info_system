import os
import uuid
from datetime import datetime

from django.db import transaction
from django.shortcuts import render, HttpResponse, redirect
from django.urls import reverse

from operateapp.models import Employee

# Create your views here.
# 显示添加员工信息的页面
def add(request):
    now = datetime.now()
    return render(request, "operateapp/addEmp.html", {"time":now})

# 显示更新员工信息页面
def update(request):
    employee_id = request.GET.get("id")
    now = datetime.now()
    employee = Employee.objects.get(pk=employee_id)
    return render(request, "operateapp/updateEmp.html", {"employee":employee,"time":now })

# 获取一个uuid
def getUUID(filename):#把一个文件的文件名传入
    id = str(uuid.uuid4())#获取一个字符串型的uuid
    extend = os.path.splitext(filename)[1]#获取文件的后缀
    # 把uuid和后缀名拼接形成新的文件名并返回
    return id + extend

# 把员工信息添加进数据库
def add_logic(request):
    name = request.POST.get("name")
    salary = request.POST.get("salary")
    age = request.POST.get("age")
    file = request.FILES.get("source")#获取图片对象
    if name == "" or salary == "" or age == "" or file == None:
        return HttpResponse("输入不能为空，请返回重新输入")
    else:
        file.name = getUUID(file.name)  # 获取一个唯一文件名
        try:
            with transaction.atomic():
                Employee.objects.create(name=name,salary=salary,age=age,headpic=file)
            return redirect("acountapp:main")
        except:
            return HttpResponse("添加失败，请返回重新添加")
# 更新员工信息
def update_logic(request):
    number = request.GET.get("num")#获取当前页码
    employee_id = request.GET.get("id")
    employee = Employee.objects.get(id=employee_id)
    name = request.POST.get("name")
    salary = request.POST.get("salary")
    age = request.POST.get("age")
    file = request.FILES.get("source")  # 获取图片对象
    if file == None:
        try:
            with transaction.atomic():
                employee.name = name
                employee.salary = salary
                employee.age = age
                employee.save()
            return redirect(reverse("acountapp:main")+"?num="+number)
        except:
            # return redirect(reverse("operateapp:update")+"?id="+employee_id)
            return render(request,"operateapp/updateEmp.html",{"employee":employee,"error_msg":"更新失败,请重新更新"})
    file.name = getUUID(file.name)  # 获取一个唯一文件名
    try:
        with transaction.atomic():
            employee.name = name
            employee.salary = salary
            employee.age = age
            employee.headpic = file
            employee.save()
        return redirect(reverse("acountapp:main")+"?num="+number)
    except:
        return render(request, "operateapp/updateEmp.html", {"employee": employee, "error_msg": "更新失败,请重新更新"})
# 删除员工信息
def delete_logic(request):
    employee_id = request.GET.get("id")
    number = request.GET.get("num")
    try:
        with transaction.atomic():
            Employee.objects.get(id=employee_id).delete()
        return redirect(reverse("acountapp:main")+"?num="+number)
    except:
        return HttpResponse("删除失败，请重新删除")

# 退出当前登录并清除cookie
def quit(request):
    rsp = redirect("acountapp:login")
    rsp.set_cookie("username", max_age=0)
    rsp.set_cookie("userpwd", max_age=0)
    return rsp



