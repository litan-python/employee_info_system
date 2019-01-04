from django.urls import path, re_path
from operateapp import views

app_name = "operateapp"

urlpatterns = [
    path("add/", views.add, name="add"),
    path("update/", views.update, name="update"),
    path("add_logic/", views.add_logic, name="add_logic"),
    path("update_logic/", views.update_logic, name="update_logic"),
    path("delete_logic/", views.delete_logic, name="delete_logic"),
    path("quit/", views.quit, name="quit"),
]