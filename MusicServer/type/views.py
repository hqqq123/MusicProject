from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from type.models import Type


@csrf_exempt
def list(request):
    infos=Type.objects.all()
    types=[]
    for info in infos:
        # types.append([info.id,info.name])
        types.append({'id':info.id,'name':info.name})

    res={'types':types}
    return JsonResponse(res)

    # res={'Types':infos}
    # return JsonResponse(serializers.serialize('json',infos),safe=False)


@csrf_exempt
def add(request):
    if request.method=='POST':
        name=request.POST['name']
        # name=request.GET.get('name',None)
        print(name,'-----------')
        if Type.objects.filter(name=name).first() is None:
            type=Type(name=name)
            type.save()
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

        type=get_object_or_404(Type, id=id)
        name=type.name
        data={'status':'ok','info':'获取成功','data':{'name':name}}
        return JsonResponse(data)
        # else:
        #     data={'status':'no','info':'失败'}
        #     return JsonResponse(data)
    else:
        id=request.POST['id']

        type=get_object_or_404(Type,id=id)
        name=request.POST['name']
        type.name=name
        type.save()
        data = {'status': 'no', 'info': '编辑成功'}
        return JsonResponse(data)

@csrf_exempt
def delete(request):
    id=request.POST['id']
    type = get_object_or_404(Type, id=id)
    type.delete()
    data = {'status': 'ok', 'info': '删除成功'}
    return JsonResponse(data=data)
