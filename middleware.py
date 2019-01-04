from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin


class MyMiddleAware(MiddlewareMixin):  # 自定义的中间件
    def __init__(self, get_response):  # 初始化
        super().__init__(get_response)

    # view处理请求前执行
    def process_request(self, request):
        # or "getCaptcha" in request.path or "check" in request.path or "query" in request.path
        if "login" in request.path or "regist" in request.path or "getCaptcha" in request.path:
            return
        if request.session.get("login") == "ok":
            return
        return redirect("acountapp:login")

        return
    # view执行之后，响应之前执行
    def process_response(self, request, response):
        return response  # 必须返回response
