import socket
import io, json
from uuid import uuid1
from minio import Minio
from django.db.models import Q
from django.http import JsonResponse
from blog.models import Blog, Blogfile
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage

client = Minio(endpoint="127.0.0.1:9000", access_key='minioadmin', secret_key="minioadmin", secure=False)

@csrf_exempt
def get_blog_single(request):
    if request.method == 'POST':
        req = json.loads(request.body)
        try:
            id = int(req['id'])
            res = Blog.objects.get(id=id)
            data = {"id": res.id, "title": res.title, "content": res.content}
            return JsonResponse({'code': 0, 'status': 'success', 'msg': "查询成功", 'data': data})
        except Exception as e:
            return JsonResponse({'code': -1, 'status': 'error', 'msg': "查询失败", 'data': {}})

@csrf_exempt
def get_blog(request):
    if request.method == 'POST':
        req = json.loads(request.body)
        currentPage = int(req["currentPage"])
        pageSize = int(req["pageSize"])
        search = req['search']
        try:
            if search:
                blog_list = Blog.objects.filter(Q(name__contains=search) | Q(content__contains=search))
            else:
                blog_list = Blog.objects.all()
            pageInator = Paginator(blog_list, pageSize)
            try:
                context = pageInator.page(currentPage)
            except EmptyPage:
                context = pageInator.page((blog_list.count()//pageSize) + 1)
            data = [{'id': item.id, 'title': item.title, 'content': item.content, 'created_at': item.created_at.strftime("%Y-%m-%d %H:%M:%S"), 'updated_at': item.updated_at.strftime("%Y-%m-%d %H:%M:%S")} for item in context]
            return JsonResponse({'code': 0, 'status': 'success', 'msg': "查询成功", 'count': blog_list.count(), 'data': data})
        except Exception as e:
            return JsonResponse({'code': -1, 'status': 'error', 'msg': "查询失败", 'data': {}})

@csrf_exempt
def create_blog(request):
    if request.method == 'POST':
        req = json.loads(request.body)
        try:
            title = req['title']
            content = req['content']
            filelist = req['filelist']

            if title.strip() == '' or content.strip() == '':
                return JsonResponse({'code': -1, 'status': 'error', 'msg': "标题或内容不能为空"})
            else:
                md = Blog.objects.create(title=title, content=content).save()
                id = md.id
                if Blogfile.objects.filter(bid=id).exists():
                    if filelist:
                        mdf = Blogfile.objects.get(bid=id)
                        mdf.file=filelist
                        mdf.save()
                    else:
                        Blogfile.objects.get(bid=id).delete()
                else:
                    if filelist:
                        Blogfile.objects.create(bid=id, file=filelist).save()
                return JsonResponse({'code': 0,'status':'success','msg': "创建成功"})
        except Exception as e:
            return JsonResponse({'code': -1, 'status': 'error', 'msg': f"创建失败{e}"})

@csrf_exempt
def update_blog(request):
    if request.method == 'POST':
        req = json.loads(request.body)
        try:
            id = req['id']
            title = req['title']
            content = req['content']
            filelist = req['filelist']
            if title.strip() == '' or content.strip() == '':
                return JsonResponse({'code': -1, 'status': 'error', 'msg': "标题或内容不能为空"})
            else:
                md = Blog.objects.get(id=id)
                md.title=title
                md.content=content
                md.save()
                if Blogfile.objects.filter(bid=id).exists():
                    if filelist:
                        md = Blogfile.objects.get(bid=id)
                        md.file=filelist
                        md.save()
                    else:
                        Blogfile.objects.get(bid=id).delete()
                else:
                    if filelist:
                        Blogfile.objects.create(bid=id, file=filelist).save()
                return JsonResponse({'code': 0, 'status': 'success', 'msg': "更新成功"})
        except Exception as e:
            return JsonResponse({'code': -1, 'status': 'error', 'msg': f"更新失败{e}"})

@csrf_exempt
def delete_blog(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        try:
            id = int(body['id'])
            Blog.objects.filter(id=id).delete()
            return JsonResponse({'code': 0, 'status': 'success', 'msg': "删除成功"})
        except Exception as e:
            return JsonResponse({'code': -1, 'status': 'error', 'msg': "删除失败"})

def remove_file(filename):
    client.remove_object("blog", filename)

@csrf_exempt
def getfile(request):
    if request.method == 'POST':
        try:
            req = json.loads(request.body)
            currentPage = int(req['currentPage'])
            pageSize = int(req['pageSize'])
            filelist = Blog.objects.all()
            pageInator = Paginator(filelist, pageSize)
            try:
                context = pageInator.page(currentPage)
            except EmptyPage:
                context = pageInator.page((filelist.count()//pageSize) + 1)
            data = [{'id': i.id, 'bid': i.bid, 'file': i.file} for i in context]
            return JsonResponse({'code': 0, 'status': 'success', 'msg': '获取成功', 'data': data})
        except Exception as e:
            return JsonResponse({'code': -1, 'status': 'error', 'msg': '获取失败'})

@csrf_exempt
def removefile(request):
    if request.method == 'POST':
        try:
            filest = [it for item in Blogfile.objects.all() for it in item.file]
            minio_filelist = [item.name for item in client.list_objects("blog")]
            for item in minio_filelist:
                if item not in filest:
                    remove_file(item)
            return JsonResponse({'code': 0, 'status': 'success', 'msg': '删除成功'})
        except Exception as e:
            return JsonResponse({'code': -1, 'status': 'error', 'msg': '删除失败'})

def getip():
    return f"{socket.gethostbyname(socket.gethostname())}:9000"

def upload_file(filename: str, file, size):
    if not client.bucket_exists("blogs"):
        client.make_bucket(bucket_name="blogs")
    client.put_object(bucket_name="blogs", object_name=filename, data=file, length=size)

@csrf_exempt
def uploadimg(request):
    if request.method == 'POST':
        try:
            files = request.FILES.getlist('file')[0]
            uid = str(uuid1())
            upload_file(f"{uid}-{files.name}", files, len(files))
            return JsonResponse({'errno': 0,  'data': {'url': f"https://weitao6.eu.org/blogs/{uid}-{files.name}", "alt": f"{uid}-{files.name}"}})#{getip()}
        except Exception as e:
            return JsonResponse({'errno': 1,  'message': "上传失败"})

@csrf_exempt
def uploadvideo(request):
    if request.method == 'POST':
        try:
            files = request.FILES.getlist('file')[0]
            uid = str(uuid1())
            upload_file(f"{uid}-{files.name}", files, len(files))
            return JsonResponse({'errno': 0,  'data': {'url': f"https://weitao6.eu.org/blogs/{uid}-{files.name}"}})
        except Exception as e:
            return JsonResponse({'errno': 1,  'message': "上传失败"})