import json

from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template import RequestContext
# Create your views here.
from django.views.decorators.csrf import  csrf_exempt

from singer.models import Singer

@csrf_exempt
def list(request):
    infos=Singer.objects.all()
    singers=[]
    for info in infos:
        # singers.append([info.id,info.name])
        singers.append({'id':info.id,'name':info.name})

    res={'singers':singers}
    return JsonResponse(res)

    # res={'singers':infos}
    # return JsonResponse(serializers.serialize('json',infos),safe=False)


@csrf_exempt
def add(request):
    if request.method=='POST':
        name=request.POST['name']
        # name=request.GET.get('name',None)
        print(name,'-----------')
        if Singer.objects.filter(name=name).first() is None:
            singer=Singer(name=name)
            singer.save()
            res={'status':'ok','info':'添加成功'}
            print(res)
            return JsonResponse(res)
        else:
            res={'status':'no','info':'添加失败！歌手已存在！'}
            return JsonResponse(res)
    else:
        res={'status':'no','info':'添加失败！请用post请求！'}
        return JsonResponse(res)

@csrf_exempt
def edit(request):
    if request.method=='GET':
        id=request.GET.get('id',None)
        if id:
            singer=get_object_or_404(Singer,id=id)
            name=singer.name
            data={'status':'ok','info':'成功','data':{'name':name}}
            return JsonResponse(data)
        else:
            data={'status':'no','info':'失败'}
            return JsonResponse(data)
    else:
        id=request.POST['id']

        singer=get_object_or_404(Singer,id=id)
        name=request.POST['name']
        singer.name=name
        singer.save()
        data = {'status': 'no', 'info': '成功'}
        return JsonResponse(data=data)

@csrf_exempt
def delete(request):
    id=request.POST['id']
    singer = get_object_or_404(Singer, id=id)
    singer.delete()
    data = {'status': 'ok', 'info': '成功'}
    return JsonResponse(data=data)
