import json

import requests
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, redirect

from django.urls import reverse

from Music.settings import URL
# Create your views here.
from account.views import is_auth, is_login


@is_login
@is_auth
def add(request):
    # message=request.GET.get('messages',None)
    # if messages is not None:
    #     messages.info(request,message)
    if request.method=='POST':
        url = URL+'type/add/'
        name=request.POST['name']
        data={"name":name}
        try:
            res=requests.post(url=url,data=data)
        except Exception as e:
            messages.info(request, '响应异常，请重新添加')
            return redirect(reverse('type_add'))
        else:
            print(json.loads(res.content.decode())['info'])
            status=json.loads(res.content.decode())['status']
            if status=='ok':
                return redirect(reverse('type_list'))
            else:
                messages.info(request, json.loads(res.content.decode())['info'])
                return redirect(reverse('type_add'))

    return render(request,'type/add.html')


@is_login
@is_auth
def list(request):
    url=URL+'type/list/'
    try:
        res=requests.get(url=url)
        res.raise_for_status()
    except Exception as e:
        messages.info(request,'获取失败')
        return redirect(reverse('base'))
    else:
        types=json.loads(res.content.decode())['types']
        li=[]
        for type in types:

            li.append({type['id']:[type['id'],type['name']]})
        types=li
        PageObj=Paginator(types,per_page=5)
        page=request.GET.get('page',1)
        typesPageObj=PageObj.page(page)
        types=typesPageObj.object_list
        return render(request, 'type/list.html', context={
            'types': types,
            'typesPageObj': typesPageObj
        })

@is_login
@is_auth
def edit(request,id):
    # pass
    # print(id)

    url=URL+'type/edit/'
    try:
        data={'id':id}
        res=requests.get(url=url,params=data)
        res.raise_for_status()
    except Exception as e:
        messages.info(request,'获取信息失败')
        return redirect(reverse('type_edit', kwargs={'id':id}))
    else:
        data=json.loads(res.text)['data']
        name=data['name']
        if request.method == 'POST':
            new_name = request.POST['name']
            # print(new_name)
            if new_name!=name and new_name:
                data={'id':id,'name':new_name}
                res=requests.post(url,data=data)
                return redirect(reverse('type_list'))
            else:
                messages.info(request, '编辑失败！未做任何修改！')
                return redirect(reverse('type_edit', kwargs={'id':id}))
        return render(request,'type/edit.html',context={
            'name':name,
            'id':id,

        })
@is_login
@is_auth
def delete(request,id):
    url=URL+'type/delete/'
    data={'id':id}
    res=requests.post(url,data=data)
    return redirect(reverse('type_list'))