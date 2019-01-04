from django.db import models

# Create your models here.
class Employee(models.Model):
    name = models.CharField(max_length=20)
    salary = models.IntegerField()
    age = models.SmallIntegerField()
    headpic = models.ImageField(upload_to="img", null=True)#存储用户头像路径，图片保存在media下的img目录中
    class Meta:
        db_table = "t_employee"