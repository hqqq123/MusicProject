from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from authority.models import Authority
from role.models import Role


@csrf_exempt
def list(request):
    roles = Role.objects.all()
    data = []
    for role in roles:
        info = {'id': role.id, 'name': role.name, 'authorities': []}
        for auth in role.authorities.all():
            info['authorities'].append(auth.name)
        data.append(info)
    return JsonResponse({'roles': data})


@csrf_exempt
def add(request):
    if request.method == 'POST':
        name = request.POST['name']
        authorities = request.POST.getlist('authorities')
        print(authorities, '-----------')
        if Role.objects.filter(name=name).first() is None:
            role = Role(name=name)
            role.save()
            for authority in authorities:
                role.authorities.add(int(authority))
            role.save()
            res = {'status': 'ok', 'info': '添加成功'}
            print(res)
            return JsonResponse(res)
        else:
            res = {'status': 'no', 'info': '添加失败！角色已存在！'}
            return JsonResponse(res)

    else:
        authorities = Authority.objects.all()
        data = {'authorities': []}
        for authority in authorities:
            data['authorities'].append({'id': authority.id, 'name': authority.name, 'url': authority.url})
        # res = {'status': 'no', 'info': '添加失败！请用post请求！'}
        return JsonResponse(data)


@csrf_exempt
def edit(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        role = get_object_or_404(Role, id=id)
        authorities = role.authorities.all()
        roleinfo={'id': id, 'name': role.name, 'authorities': []}

        for auth in authorities:
            roleinfo['authorities'].append(auth.id)

        data = {'role': roleinfo, 'authorities': []}

        authorities = Authority.objects.all()
        for authority in authorities:
            data['authorities'].append({'id': authority.id, 'name': authority.name, 'url': authority.url})
        print(data)
        return JsonResponse(data)
    else:
        id = request.POST['id']
        authorities=request.POST.getlist('authorities')
        print(authorities)
        role = get_object_or_404(Role, id=id)

        name = request.POST['name']
        if name!=role.name and Role.objects.filter(name=name).first:
            data = {'status': 'no', 'info': '编辑失败！角色名已存在！'}
            return JsonResponse(data=data)

        role.name = name
        if role.authorities!=authorities:
            role.authorities.clear()
            for auth in authorities:
                role.authorities.add(auth)
        role.save()
        data = {'status': 'ok', 'info': '成功'}
        return JsonResponse(data=data)


@csrf_exempt
def delete(request):
    id = request.POST['id']
    role = get_object_or_404(Role, id=id)
    role.delete()
    data = {'status': 'ok', 'info': '成功'}
    return JsonResponse(data=data)
