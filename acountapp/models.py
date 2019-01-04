from django.db import models

# Create your models here.
#保存职工的账号信息
class Acount(models.Model):
    username = models.CharField(max_length=20, unique=True)#用户名
    realname = models.CharField(max_length=20)#真实姓名
    userpwd = models.CharField(max_length=20)#登录密码
    sex = models.CharField(max_length=20)#性别
    class Meta:
        db_table = "t_acount"
