from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from authority.models import Authority

@csrf_exempt
def add(request):
    name = request.POST['name']
    # return JsonResponse({'status': 'ok', 'info': '成功'})

    url = request.POST['url']
    #
    if Authority.objects.filter(name=name).first() is not None:
        return JsonResponse({'status': 'no', 'info': '该权限已经存在'})
    else:
        authority = Authority(name=name, url=url)
        authority.save()
        return JsonResponse({'status': 'ok', 'info': '成功'})

@csrf_exempt
def list(request):
    authorities = Authority.objects.all()
    data = {'authorities': []}
    for authority in authorities:
        data['authorities'].append({'id': authority.id, 'name': authority.name,'url':authority.url})

    return JsonResponse(data)
@csrf_exempt
def edit(request):
    name = request.POST['name']
    if Authority.objects.filter(name=name).first() is not None:
        return JsonResponse({'status': 'no', 'info': '该权限名已经存在'})
    else:
        url = request.POST['url']
        id = request.POST['id']


        authority = get_object_or_404(Authority,id=id)
        authority.name=name
        authority.url=url
        authority.save()
        return JsonResponse({'status': 'ok', 'info': '成功'})

@csrf_exempt
def delete(request):
    id=request.POST['id']
    authority = get_object_or_404(Authority, id=id)
    authority.delete()
    data = {'status': 'ok', 'info': '成功'}
    return JsonResponse(data=data)
