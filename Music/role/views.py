import json

import requests
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse

from Music.settings import URL
from account.views import is_login, is_auth


@is_login
@is_auth
def list(request):
    url=URL+'role/list/'
    res=requests.post(url,data={'id':id})
    print(res.headers,'------------------------')
    roles=json.loads(res.text)['roles']
    PageObj=Paginator(roles,per_page=5)
    page=request.GET.get('page',1)
    rolesPageObj=PageObj.page(page)
    roles=rolesPageObj.object_list

    return render(request,'role/list.html',context={
        'roles':roles,
        'rolesPageObj':rolesPageObj,
    })

@is_login
@is_auth
def add(request):
    url=URL+'role/add/'
    res=requests.get(url)
    authorities=json.loads(res.text)['authorities']
    if request.method=='POST':
        name=request.POST['name']
        authorities=request.POST.getlist('authorities')
        # print(authorities)
        data={'name':name,'authorities':authorities}

        url=URL+'role/add/'
        res=requests.post(url,data=data)
        res=json.loads(res.text)
        if res['status']=='ok':
            return redirect(reverse('role_list'))
        else:
            messages.info(request,res['info'])
            return redirect(reverse('role_add'))

    return render(request,'role/add.html',context={
        'authorities':authorities,
    })
@is_login
@is_auth
def edit(request,id):
    # if request.method=='GET':
    # print('-------------')
    url=URL+'role/edit/'
    res=requests.get(url,params={'id':id})
    data=json.loads(res.text)
    role=data['role']
    authorities=data['authorities']

    if request.method == 'POST':
        url = URL + 'role/edit/'
        res = requests.get(url, params={'id': id})
        data = json.loads(res.text)
        role = data['role']
        old_authorities=role['authorities']



        new_name = request.POST['name']

        authorities=[int(auth) for auth in request.POST.getlist('authorities')]
        print(old_authorities)
        print(authorities)
        if new_name != role['name'] or new_name or old_authorities != authorities :
            data = {'id': id, 'name': new_name, 'authorities': authorities}

            res = requests.post(url, data=data)
            return redirect(reverse('role_list'))
        else:
            messages.info(request, '编辑失败！未做任何修改！')
            return redirect(reverse('role_edit', args=[id, ]))
    return render(request,'role/edit.html',context={
        'role':role,
        'authorities':authorities,
    })
@is_login
@is_auth
def delete(request,id):
    url=URL+'role/delete/'
    data={'id':id}
    res=requests.post(url,data=data)
    return redirect(reverse('role_list'))
@is_login
@is_auth
def authorities(request,id):
    url=URL+'role/authorities/'
    res=requests.post(url,data={'id':id})

    authorities=json.loads(res.text)['authorities']
