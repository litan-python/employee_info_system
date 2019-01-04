from django.urls import path

from acountapp import views

app_name = "acountapp"
urlpatterns = [
    path("login/", views.login, name="login"),
    path("main/", views.main, name="main"),
    path("login_logic/", views.login_logic, name="login_logic"),
    path("regist/", views.regist, name="regist"),
    path("regist_logic/", views.regist_logic, name="regist_logic"),
    path("getCaptcha/", views.getCaptcha, name="getCaptcha"),
    path("checkname/", views.checkname, name="checkname"),
    path("checkcode/", views.checkcode, name="checkcode"),
    path("query/", views.query, name="query"),
]