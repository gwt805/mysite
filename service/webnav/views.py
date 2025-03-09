import json
from loguru import logger
from natsort import natsorted
from django.http import JsonResponse
from webnav.models import Webnav, Webnavlabel
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage

@csrf_exempt
def webnavlabel_get_single(request):
    if request.method == 'POST':
        req = json.loads(request.body)
        try:
            id = int(req.get('id'))
            webnavlabel = Webnavlabel.objects.get(id=id)
            data = {'id': webnavlabel.id, 'tag': webnavlabel.tag}
            return JsonResponse({'code': 0, 'status': "success", 'msg': "查询成功", 'data': data})
        except Exception as e:
            return JsonResponse({'code': -1, 'status': "error", 'msg': "查询失败"})

@csrf_exempt
def webnavlabel_upd_single(request):
    if request.method == 'POST':
        req = json.loads(request.body)
        try:
            id = int(req.get('id'))
            tag = req.get('tag').strip()
            if tag == '':
                return JsonResponse({'code': -1, 'status': "error", 'msg': "标签不能为空"})
            webnavlabel = Webnavlabel.objects.get(id=id)
            Webnavlabel.objects.filter(tag=webnavlabel.tag).update(tag=tag)
            webnavlabel.tag = tag
            webnavlabel.save()
            return JsonResponse({'code': 0, 'status': "success", 'msg': "更新成功"})
        except Exception as e:
            return JsonResponse({'code': -1, 'status': "error", 'msg': "更新失败"})

@csrf_exempt
def webnavlabel_del_single(request):
    if request.method == 'POST':
        req = json.loads(request.body)
        try:
            id = int(req.get('id'))
            webnavlabel = Webnavlabel.objects.get(id=id)
            webnavs = Webnav.objects.filter(tag=webnavlabel.tag).exists()
            if webnavs:
                return JsonResponse({'code': -1, 'status': "error", 'msg': "该标签下存在导航，无法删除"})
            else:
                webnavlabel.delete()
                return JsonResponse({'code': 0, 'status': "success", 'msg': "删除成功"})
        except Exception as e:
            return JsonResponse({'code': -1, 'status': "error", 'msg': "删除失败"})

@csrf_exempt
def webnavlabel_add(request):
    if request.method == 'POST':
        req = json.loads(request.body)
        try:
            tag = req.get('tag')
            if tag == '': return JsonResponse({'code': -1, 'status': "error", 'msg': "标签不能为空"})
            Webnavlabel.objects.create(tag=tag)
            return JsonResponse({'code': 0, 'status': "success", 'msg': "添加成功"})
        except Exception as e:
            return JsonResponse({'code': -1, 'status': "error", 'msg': "添加失败"})

@csrf_exempt
def webnavlabel_get(request):
    if request.method == 'POST':
        req = json.loads(request.body)
        type = req.get('type')
        search = req.get('search')
        currentPage = req.get('currentPage')
        pageSize = req.get('pageSize')
        if type == 'label':
            if search: webnavlabels = Webnavlabel.objects.filter(tag__icontains=search).order_by('id')
            else: webnavlabels = Webnavlabel.objects.all().order_by('id')
        else:
            webnavlabels = Webnavlabel.objects.all().order_by('id')
        data = []
        if type == 'label':
            pageInator = Paginator(webnavlabels, pageSize)
            try:
                context = pageInator.page(currentPage)
            except EmptyPage:
                context = pageInator.page((webnavlabels.count()//pageSize) + 1)
            for item in context:
                data.append({'id': item.id, 'tag': item.tag})
        else:
            for item in webnavlabels:
                data.append({'id': item.id, 'tag': item.tag})

        return JsonResponse({'code': 0, 'status': "success", 'msg': "查询成功", 'count': webnavlabels.count(), 'data': data})

# ----------------------------------------------------------------------------------------------------

@csrf_exempt
def webnav(request):
    if request.method == 'POST':
        search = json.loads(request.body).get('search')
        webnavs = Webnav.objects.filter(name__icontains=search)
        if not search: webnavs = natsorted(list(set(webnavs.values_list('tag'))))
        data = []
        search_data = []
        for item in webnavs:
            if not search: 
                webnav = Webnav.objects.filter(tag=item[0])
                data.append({'tag': item[0], 'body': list(webnav.values())})
            else:
                logger.info(item)
                search_data.append({'name': item.name, 'weburl': item.weburl, 'imgurl': item.imgurl, 'tooltip': item.tooltip, 'tag': item.tag})
        if search: data.append({'tag': "", 'body': search_data})
        return JsonResponse({'code': 0, 'status': "success", 'msg': "查询成功", 'data': data})

@csrf_exempt
def cwebnav_get_single(request):
    if request.method == 'POST':
        req = json.loads(request.body)
        try:
            id = int(req.get('id'))
            webnavs = Webnav.objects.filter(id=id)
            data = []
            for item in webnavs:
                data.append({'id': item.id, 'name': item.name, 'weburl': item.weburl, 'imgurl': item.imgurl, 'tooltip': item.tooltip, 'tag': item.tag})
            return JsonResponse({'code': 0, 'status': "success", 'msg': "查询成功", 'data': data[0]})
        except Exception as e:
            return JsonResponse({'code': -1, 'status': "error", 'msg': f"查询失败{e}",})

@csrf_exempt
def cwebnav_upd_single(request):
    if request.method == 'POST':
        req = json.loads(request.body)
        try:
            id = int(req.get('id'))
            name = req.get('name')
            weburl = req.get('weburl')
            imgurl = req.get('imgurl')
            tooltip = req.get('tooltip')
            tag = req.get('tag')
            webnav = Webnav.objects.get(id=id)
            webnav.name = name
            webnav.weburl = weburl
            webnav.imgurl = imgurl
            webnav.tooltip = tooltip
            webnav.tag = tag
            webnav.save()
            return JsonResponse({'code': 0, 'status': "success", 'msg': "更新成功"})
        except Exception as e:
            return JsonResponse({'code': -1, 'status': "error", 'msg': f"更新失败{e}"})

@csrf_exempt
def cwebnav_del_single(request):
    if request.method == 'POST':
        req = json.loads(request.body)
        try:
            id = int(req.get('id'))
            webnavs = Webnav.objects.get(id=id)
            webnavs.delete()
            return JsonResponse({'code': 0, 'status': "success", 'msg': "删除成功"})
        except Exception as e:
            return JsonResponse({'code': -1, 'status': "error", 'msg': f"删除失败{e}"})

@csrf_exempt
def cwebnav_get(request):
    if request.method == 'POST':
        req = json.loads(request.body)
        search = req.get('search')
        currentPage = int(req.get('currentPage'))
        pageSize = int(req.get('pageSize'))
        if search: webnavs = Webnav.objects.filter(name__icontains=search)
        else: webnavs = Webnav.objects.all()
        pageInator = Paginator(webnavs, pageSize)
        try:
            context = pageInator.page(currentPage)
        except EmptyPage:
            context = pageInator.page((webnavs.count()//pageSize) + 1)
        data = []
        for item in context:
            data.append({'id': item.id, 'name': item.name, 'weburl': item.weburl, 'imgurl': item.imgurl, 'tooltip': item.tooltip, 'tag': item.tag})
        return JsonResponse({'code': 0, 'status': "success", 'msg': "查询成功",'count': webnavs.count() ,'data': data})

@csrf_exempt
def cwebnav_add(request):
    if request.method == 'POST':
        req = json.loads(request.body)
        try:
            name = req.get('name').strip()
            weburl = req.get('weburl').strip()
            imgurl = req.get('imgurl').strip()
            tooltip = req.get('tooltip').strip()
            tag = req.get('tag').strip()
            Webnav.objects.create(name=name, weburl=weburl, imgurl=imgurl, tooltip=tooltip, tag=tag)
            return JsonResponse({'code': 0, 'status': "success", 'msg': "添加成功"})
        except Exception as e:
            return JsonResponse({'code': -1, 'status': "error", 'msg': f"添加失败{e}"})