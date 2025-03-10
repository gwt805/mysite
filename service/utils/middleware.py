from .token import check_token
from django.http import JsonResponse
from loguru import logger
try:
    from django.utils.deprecation import MiddlewareMixin  # Django 1.10.x
except ImportError:
    MiddlewareMixin = object

# 白名单，表示请求里面的路由时不验证登录信息
API_WHITELIST = [
    "/qqbot/",
    "/api/webnav/",
    "/api/systeminfo/",
    "/api/auth/login/",
    "/api/blog/getblog/",
    "/api/blog/getblog_single/",
]

class AuthorizeMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path not in API_WHITELIST:
            if "sites" in request.path:
                pass
            else:
                # 从请求头中获取 username 和 token
                token = request.META.get("HTTP_AUTHORIZATION")
                if token is None:
                    return JsonResponse({"code": -2, "msg": "登录信息错误或已过期"})
                if check_token(token):
                    pass
                else:
                    return JsonResponse({"code": -2, "msg": "登录信息错误或已过期"})
