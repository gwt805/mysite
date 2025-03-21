import os
import json
import random
import requests
from nacl import signing
from loguru import logger
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

APP_ID = os.getenv('APP_ID', "") # your appID
BOT_SECRET = os.getenv('BOT_SECRET', "") # your secret
processed_message_ids = set()

logger.info(f"APP_ID: {APP_ID} BOT_SECRET: {BOT_SECRET}")

@csrf_exempt
def qqbot(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        logger.info(data)

        if not data: return JsonResponse({"error": "Invalid request"})
        if data.get("op") == 13:
            validation_payload = data.get("d", {})
            plain_token = validation_payload.get("plain_token")
            event_ts = validation_payload.get("event_ts")

            if not plain_token or not event_ts: return JsonResponse({"error": "Missing required fields"})

            signature = generate_ed25519_signature(plain_token, event_ts, BOT_SECRET)
            return JsonResponse({"plain_token": plain_token, "signature": signature})
        else:
            event_type = data.get("t")
            message = data.get("d", {})
            if event_type == "C2C_MESSAGE_CREATE":
                openid = message["author"]["id"]
                content = message["content"].strip()
                msg_id = message["id"]
                is_success =  process_message('private', openid, content, msg_id)
                if is_success: return JsonResponse({"status": "Message sent successfully"})
                else: return JsonResponse({"error": "Failed to send message"})
            elif event_type == "GROUP_AT_MESSAGE_CREATE":
                group_openid = message["group_openid"]
                content = message["content"].strip()
                msg_id = message["id"]
                is_success = process_message('group', group_openid, content, msg_id)
                if is_success: return JsonResponse({"status": "Message sent successfully"})
                else: return JsonResponse({"error": "Failed to send message"})
            else:
                return JsonResponse({"error": "Unknown event"})

def generate_ed25519_signature(plain_token, event_ts, secret):
    sign_str = f"{event_ts}{plain_token}".encode() # 拼接待签名的字符串
    signing_key = signing.SigningKey(secret.encode()) # 生成私钥
    signed_message = signing_key.sign(sign_str)
    signature = signed_message.signature.hex() # 生成签名
    return signature

def get_access_token():
    # url = "https://qqbot-token.weilong.workers.dev/app/getAppAccessToken" # pythonanywhere + cloudflare
    url = "https://bots.qq.com/app/getAppAccessToken"
    headers = {"Content-Type": "application/json"}
    data = {"appId": APP_ID, "clientSecret": BOT_SECRET}
    response = requests.post(url, headers=headers, json=data)
    logger.info(response.json().get("access_token"))
    if response.status_code == 200: return response.json().get("access_token")
    else: return None

def send_private_message(openid, msg_type, content_type, content, msg_id=None): # 单聊
    access_token = get_access_token()
    if not access_token: return False
    # url = f"https://qqbot-msg.weilong.workers.dev/v2/users/{openid}/messages" # pythonanywhere + cloudflare
    url = f"https://sandbox.api.sgroup.qq.com/v2/users/{openid}/messages" # 正式环境去掉 sandbox
    headers = {"Authorization": f"QQBot {access_token}", "Content-Type": "application/json"}
    data = {"msg_type": msg_type, f"{content_type}": content}
    if msg_type == 7: data['content'] = " "
    if msg_id: data["msg_id"] = msg_id

    response = requests.post(url, headers=headers, json=data)
    logger.info(response.json())

    if response.status_code == 200:
        logger.info('private send message success')
        if msg_id in processed_message_ids:
            processed_message_ids.remove(msg_id)
        return True
    else:
        logger.info(f'private send message failed')
        if msg_id in processed_message_ids:
            processed_message_ids.remove(msg_id)
        return False

def send_group_message(group_openid, msg_type, content_type, content, msg_id=None): # 群聊
    access_token = get_access_token()
    if not access_token: return False
    # url = f"https://qqbot-msg.weilong.workers.dev/v2/groups/{group_openid}/messages" # pythonanywhere + cloudflare
    url = f"https://sandbox.api.sgroup.qq.com/v2/groups/{group_openid}/messages" # 正式环境去掉 sandbox
    headers = {"Authorization": f"QQBot {access_token}", "Content-Type": "application/json"}
    data = {"msg_type": msg_type, f"{content_type}": content}
    if msg_type == 7: data['content'] = " "
    if msg_id: data["msg_id"] = msg_id

    response = requests.post(url, headers=headers, json=data)
    logger.info(response.json())

    if response.status_code == 200:
        logger.info('group send message success')
        if msg_id in processed_message_ids:
            processed_message_ids.remove(msg_id)
        return True
    else:
        logger.info('group send message failed')
        if msg_id in processed_message_ids:
            processed_message_ids.remove(msg_id)
        return False

def upload_media(upload_type, openid, file_type, media_url):
    access_token = get_access_token()
    if not access_token:
        logger.error("Failed to get access token.")
        return None

    url = f"https://sandbox.api.sgroup.qq.com/v2/{upload_type}/{openid}/files"
    headers = {"Authorization": f"QQBot {access_token}", "Content-Type": "application/json"}
    data = {
        "file_type": file_type,
        "url": media_url,
        "srv_send_msg": False  # 不直接发送，获取 file_info
    }

    response = requests.post(url, headers=headers, json=data)
    logger.info(response.json())
    if response.status_code == 200:
        file_info = response.json().get("file_info")
        logger.info(f"Media uploaded successfully: {file_info}")
        return file_info
    else:
        logger.error(f"Failed to upload media: {response.json()}")
        return None

def process_message(msg_type, openid, content, msg_id):
    global processed_message_ids
    if msg_id in processed_message_ids:
        logger.info(f"Message {msg_id} already processed, skipping")
        return True
    processed_message_ids.add(msg_id)

    if content == "" or content == '/help':
        logger.info('process message help')
        mk = "\n我是机器人 AIRobot\n\n指令列表\n    1. /AI+空格+问题\n    2. /天气+空格+市级地区\n    3. /help\n    4. /随机图片\n\n如需添加其他功能，请联系群主"
        if msg_type == 'group': return send_group_message(openid, 0, 'content', mk, msg_id)
        if msg_type == 'private': return send_private_message(openid, 0,'content',  mk, msg_id)
    elif content.startswith("/天气"):
        logger.info('process message weather')
        if (content.split("/天气 ")) == 1:
            if msg_type == 'group': return send_group_message(openid, 0, 'content', '\n请输入城市名', msg_id)
            if msg_type == 'private': return send_private_message(openid, 0, 'content', '请输入城市名', msg_id)
        else:
            city = content.split("/天气 ")[1]
            if city == '':
                if msg_type == 'group': return send_group_message(openid, 0, 'content', '\n请输入城市名', msg_id)
                if msg_type == 'private': return send_private_message(openid, 0, 'content', '请输入城市名', msg_id)
            else:
                try:
                    res = requests.get(f"https://v.api.aa1.cn/api/api-weather/qq-weather.php?msg={city}").text
                    res = str(res)[str(res).index("城"):]
                    logger.info(f"weather res: {res}")
                    if msg_type == 'group': return send_group_message(openid, 0, 'content', "\n" + res, msg_id)
                    if msg_type == 'private': return send_private_message(openid, 0, 'content', res, msg_id)
                except:
                    if msg_type == 'group': return send_group_message(openid, 0, 'content', "\n天气获取失败", msg_id)
                    if msg_type == 'private': return send_private_message(openid, 0, 'content', "天气获取失败", msg_id)
    elif content.startswith("/AI"):
        logger.info('process message AI')
        if (content.split("/AI ")) == 1:
            if msg_type == 'group': return send_group_message(openid, 0, 'content', '\n请输入问题', msg_id)
            if msg_type == 'private': send_private_message(openid, 0, 'content', '请输入问题', msg_id)
        else:
            question = content.split("/AI ")[1]
            if question == '':
                if msg_type == 'group': return send_group_message(openid, 0, 'content', '\n请输入问题', msg_id)
                if msg_type == 'private': return send_private_message(openid, 0, 'content', '请输入问题', msg_id)
            else:
                try:
                    res = requests.post(f"https://tools.mgtv100.com/external/v1/pear/deepseek", {'content': question}).json()
                    logger.info(f"AI res: {res}")
                    if msg_type == 'group': return send_group_message(openid, 0, 'content', "\n" + str(res['data']['message']), msg_id)
                    if msg_type == 'private': return send_private_message(openid, 0, 'content',  str(res['data']['message']), msg_id)
                except:
                    if msg_type == 'group': return send_group_message(openid, 0, 'content', "\n结果获取失败", msg_id)
                    if msg_type == 'private': return send_private_message(openid, 0, 'content', "结果获取失败", msg_id)
    elif content == "/随机图片":
        logger.info('process message random image')
        try:
            res = requests.get(f"https://api.acgurl.link/img?type={random.choice(['ysh', 'yss', 'xqh', 'xqs', 'bing'])}&json=true").json()
            logger.info(f"random image res: {res}")
            if msg_type == 'group':
                if "url" in res:
                    file_info = upload_media('groups' ,openid, file_type=1, media_url=res["url"])
                    if file_info:
                        return send_group_message(openid, 7, "media", {'file_type': 1, 'file_info': file_info, 'srv_send_msg': False}, msg_id)
                    else:
                        return send_group_message(openid, 0, "content", "\图片获取失败", msg_id)
                else:
                    return send_group_message(openid, 0, "content", "\图片获取失败", msg_id)
                return send_group_message(openid, 7, 'media', {'file_type': 1, 'url': res['url'], 'srv_send_msg': True}, msg_id)
            if msg_type == 'private':
                if "url" in res:
                    file_info = upload_media('users' ,openid, file_type=1, media_url=res["url"])
                    if file_info:
                        return send_private_message(openid, 7, "media", {'file_type': 1, 'file_info': file_info, 'srv_send_msg': False}, msg_id)
                    else:
                        return send_private_message(openid, 0, "content", "\图片获取失败", msg_id)
                else:
                    return send_private_message(openid, 0, "content", "\图片获取失败", msg_id)
        except:
            if msg_type == 'group':
                return send_group_message(openid, 0, 'content', "\n图片获取失败", msg_id)
            if msg_type == 'private':
                return send_private_message(openid, 0, 'content', "图片获取失败", msg_id)
    else:
        logger.info('process message unknown')
        if msg_type == 'group':
            return send_group_message(openid, 0, 'content', '\n未知指令，请使用 /help 查看指令大全', msg_id)
        if msg_type == 'private':
            return send_private_message(openid, 0, 'content', '未知指令，请使用 /help 查看指令大全', msg_id)
