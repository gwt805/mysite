import json
import hashlib
from loguru import logger
from django.http import JsonResponse
from utils.token import create_token
from django.views.decorators.csrf import csrf_exempt

def checkauth(username, password):
    hash_algorithm = hashlib.sha256()
    user = username.encode("utf-8")
    hash_algorithm.update(user)
    user_c = hash_algorithm.hexdigest()
    pwd = password.encode("utf-8")
    hash_algorithm.update(pwd)
    pwd_c = hash_algorithm.hexdigest()
    return user_c, pwd_c

@csrf_exempt
def login(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")
        user, pwd = checkauth(username, password)
        if user == "c3ef28adf348a58ac42e9c9a41bd39007735deb54b7b21557acb3465d3173a86" and pwd == "17bacc87a7b20a532abe1713cb5d7c598ef2a2e7516d32d17f699ed5ad78a87f":
            token = create_token()
            return JsonResponse({"code": 0, "status": "successful", "msg": "登录成功", "token": token})
        else:
            return JsonResponse({"code": -1, "status": "error", "msg": "账号或密码错误!"})