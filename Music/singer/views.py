import json
import socket
from concurrent.futures import ThreadPoolExecutor, wait

import requests
from django.contrib import messages
from django.core.paginator import Paginator
from django.db import connection
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from Music.settings import URL
from account.views import is_auth, is_login
from singer.models import Singer

def base(request):

    return render(request, 'base.html')

# @csrf_exempt


@is_login
@is_auth
def add(request):
    # message=request.GET.get('messages',None)
    # if messages is not None:
    #     messages.info(request,message)
    if request.method=='POST':
        url = URL+'singer/add/'
        name=request.POST['name']
        data={"name":name}
        try:
            res=requests.post(url=url,data=data)
        except Exception as e:
            messages.info(request, '响应异常，请重新添加')
            return redirect(reverse('singer_add'))
        else:
            print(json.loads(res.content.decode())['info'])
            status=json.loads(res.content.decode())['status']
            if status=='ok':
                return redirect(reverse('singer_list'))
            else:
                messages.info(request, json.loads(res.content.decode())['info'])
                return redirect(reverse('singer_add'))

    return render(request,'singer/add.html')
@is_login
@is_auth
def list(request):
    url=URL+'singer/list/'
    try:
        res=requests.get(url=url)
        res.raise_for_status()
    except Exception as e:
        messages.info(request,'获取失败')
        return redirect(reverse('music_list'))
    else:
        singers=json.loads(res.content.decode())['singers']
        li=[]
        for singer in singers:

            li.append({singer['id']:[singer['id'],singer['name']]})
        singers=li
        PageObj=Paginator(singers,per_page=5)
        page=request.GET.get('page',1)
        singersPageObj=PageObj.page(page)
        singers=singersPageObj.object_list
        return render(request, 'singer/list.html', context={
            'singers': singers,
            'singersPageObj': singersPageObj
        })

@is_login
@is_auth
def edit(request,id):
    # print(id)


    url=URL+'singer/edit/'
    try:
        data={'id':id}
        res=requests.get(url=url,params=data)
        res.raise_for_status()
    except Exception as e:
        messages.info(request,'获取信息失败')
        return redirect(reverse('singer_edit', args=[id, ]))
    else:
        data=json.loads(res.text)['data']
        name=data['name']
        if request.method == 'POST':
            new_name = request.POST['name']
            # print(new_name)
            if new_name!=name and new_name:
                data={'id':id,'name':new_name}
                res=requests.post(url,data=data)
                return redirect(reverse('singer_list'))
            else:
                messages.info(request, '编辑失败！未做任何修改！')
                return redirect(reverse('singer_edit', args=[id, ]))
        return render(request,'singer/edit.html',context={
            'name':name,
            'id':id,

        })
@is_login
@is_auth
def delete(request,id):
    url=URL+'singer/delete/'
    data={'id':id}
    res=requests.post(url,data=data)
    return redirect(reverse('singer_list'))
