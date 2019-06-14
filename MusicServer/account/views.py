from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from account.models import Account
from role.models import Role

@csrf_exempt
def list(request):
    infos=Account.objects.all()
    print(infos)
    accounts=[]
    for info in infos:
        # print(info.role)
        # singers.append([info.id,info.name])
        if info.role:

            accounts.append({'id':info.id,'name':info.name,'role_id':info.role.id,'role_name':info.role.name})
        else:
            accounts.append({'id': info.id, 'name': info.name, 'role_id': None, 'role_name': None})

    res={'accounts':accounts}
    return JsonResponse(res)
@csrf_exempt
def add(request):
    if request.method=='GET':
        roles=Role.objects.all()
        data={'roles':[]}
        for role in roles:
            data['roles'].append({'id':role.id,'name':role.name})
        return JsonResponse(data)
    else:
        name=request.POST['name']
        if Account.objects.filter(name=name).first() is None:
            pwd = request.POST['password']
            role=request.POST['role']
            pwd = make_password(pwd)
            role=get_object_or_404(Role,id=role)
            account=Account(name=name,password=pwd,role=role)
            account.save()
            res={'status':'ok','info':'添加成功'}
            # print(res)
            return JsonResponse(res)
        else:
            res={'status':'no','info':'添加失败！用户已存在！'}
            return JsonResponse(res)
@csrf_exempt
def delete(request):
    id=request.POST['id']
    account = get_object_or_404(Account, id=id)
    account.delete()
    data = {'status': 'ok', 'info': '成功'}
    return JsonResponse(data=data)
@csrf_exempt
def edit(request):
    if request.method=='GET':
        id=request.GET.get('id',None)

        account=get_object_or_404(Account,id=id)
        data={'account':{'id':account.id,'name':account.name,'role_id':account.role.id,'role_name':account.role.name},'roles':[]}

        roles=Role.objects.all()
        for role in roles:
            data['roles'].append({'id':role.id,'name':role.name})
        # data={'status':'ok','info':'成功','data':}
        return JsonResponse(data)
    else:

        name=request.POST['name']
        id=request.POST['id']
        account=Account.objects.filter(id=id).first()

        if account.name==name or Account.objects.filter(name=name).first() is None:
            # id = request.POST['id']
            # account = get_object_or_404(Account, id=id)
            account.name = name
            role=request.POST['role']
            role=get_object_or_404(Role,id=role)
            account.role=role
            account.save()
            data = {'status': 'ok', 'info': '成功'}
            return JsonResponse(data=data)

        else:
            res={'status':'no','info':'修改失败！用户已存在！'}
            return JsonResponse(res)

@csrf_exempt
def pwd(request):

    if request.method=='GET':
        id=request.GET.get('id',None)

        account=get_object_or_404(Account,id=id)
        data={'account':{'id':account.id,'name':account.name,'password':account.password}}
        return JsonResponse(data=data)
    else:
        id=request.POST['id']
        pwd=request.POST['password']
        account=get_object_or_404(Account,id=id)
        account.password=make_password(pwd)
        account.save()
        data = {'status': 'ok', 'info': '成功'}
        return JsonResponse(data=data)


@csrf_exempt
def login(request):
    name=request.POST['name']
    account=Account.objects.filter(name=name).first()
    # account=get_object_or_404(Account,name=name)
    if account:
        password=request.POST['password']
        if check_password(password,account.password):
            return JsonResponse({'status':'ok','info':'校验成功','id':account.id})
        else:
            return JsonResponse({'status':'no','info':'密码错误'})
    else:
        return JsonResponse({'status': 'no', 'info': '用户不存在'})

@csrf_exempt
def auths(request):
    print('---===')
    id=request.POST['id']
    account=Account.objects.filter(id=id).first()
    auths=account.role.authorities.all()
    data={'auths':[]}
    for auth in auths:
        data['auths'].append(auth.url)
    print(data,'---------------')
    return JsonResponse(data)

@csrf_exempt
def name(request):
    name = request.POST['name']
    id = request.POST['id']


    if Account.objects.filter(name=name).first() is None:
        # id = request.POST['id']
        # account = get_object_or_404(Account, id=id)
        account = Account.objects.filter(id=id).first()
        account.name = name
        account.save()
        data = {'status': 'ok', 'info': '成功'}
        return JsonResponse(data=data)

    else:
        res = {'status': 'no', 'info': '修改失败！用户已存在！'}
        return JsonResponse(res)