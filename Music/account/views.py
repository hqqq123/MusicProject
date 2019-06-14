import json
from functools import wraps

import requests
from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
from django.core.paginator import Paginator
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse

from Music.settings import URL

def is_login(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        user = request.session.get("user", None)
        # print(user)
        if user:
            return func(request, *args, **kwargs)
        else:
            messages.error(request, "用户未登录,请先登录！")

            return redirect(reverse('account_login'))

    return wrapper

def is_auth(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        # if not request.user.is_authenticated():
        #     return redirect(reverse('login'))
        # print('============')
        id = request.session.get('user_id', None)
        # print(id)

        _url = URL + 'account/auths/'
        res = requests.post(_url, data={'id': id})
        # print(res.text)
        urls = json.loads(res.text)['auths']
        print(urls, '***********************')
        url = request.path_info
        print(url, '------------------------')
        if url.find('/edit/') >= 0:
            url = url.split('/edit/')[0] + '/edit/'
        elif url.find('/delete/') >= 0:
            url = url.split('/delete/')[0] + '/delete/'
        elif url.find('/pwd/') >= 0:
            url = url.split('/pwd/')[0] + '/pwd/'
        elif url.find('/musiclist/music/add/') >= 0:
            url = url.split('/musiclist/music/add/')[0] + '/musiclist/music/add/'
            print(url)
        else:
            url = url
        print(url)
        if url in urls:

            return func(request, *args, **kwargs)
        else:
            messages.info(request, '当前用户没有权限!')
            return redirect(reverse('music_list'))
        # except Exception as e:
        #     print(e, '===============================------------')
        #     return redirect(reverse('music_list'))

    return wrapper

@is_login
@is_auth
def list(request):
    url = URL + 'account/list/'
    res = requests.get(url)
    accounts = json.loads(res.text)['accounts']
    PageObj = Paginator(accounts, per_page=5)
    page = request.GET.get('page', 1)
    accountsPageObj = PageObj.page(page)
    accounts = accountsPageObj.object_list

    return render(request, 'account/list.html', context={
        'accounts': accounts,
        'accountsPageObj': accountsPageObj,
    })

@is_login
@is_auth
def add(request):
    url = URL + 'account/add/'
    res = requests.get(url)
    roles = json.loads(res.text)['roles']
    if request.method == 'POST':
        name = request.POST['name']
        pwd = request.POST['pwd']
        role = request.POST['role']

        res = requests.post(url, data={'name': name, 'password': pwd, 'role': int(role)})
        res = json.loads(res.text)
        if res['status'] == 'ok':
            return redirect(reverse('account_list'))
        else:
            messages.info(request, res['info'])
            return redirect(reverse('account_add'))
    return render(request, 'account/add.html', context={
        'roles': roles,
    })

@is_login
@is_auth
def delete(request, id):
    url = URL + 'account/delete/'
    data = {'id': id}
    if id==request.session.get('user_id'):
        del request.session['user']
        del request.session['user_id']

    res = requests.post(url, data=data)
    return redirect(reverse('account_list'))

@is_login
@is_auth
def edit(request, id):
    url = URL + 'account/edit/'
    res = requests.get(url, params={'id': id})
    data = json.loads(res.text)
    account = data['account']
    roles = data['roles']

    if request.method == 'POST':
        url = URL + 'account/edit/'
        res = requests.get(url, params={'id': id})
        data = json.loads(res.text)
        account = data['account']
        roles = data['roles']

        new_name = request.POST['name']
        old_name= account['name']
        role = request.POST['role']
        print(new_name, role)
        if new_name != old_name or int(role) != account['role_id']:
            data = {'id': id, 'name': new_name, 'role': int(role)}
            res = requests.post(url, data=data)
            print('2222222222222222')
            res = json.loads(res.text)
            if res['status'] == 'ok':
                if new_name != old_name:
                    print('1111111111111111')
                    request.session['user'] = new_name
                    print('333333333333333333333',)
                return redirect(reverse('account_list'))
            else:


                messages.info(request, res['info'])
                return redirect(reverse('account_edit', kwargs={'id': id}))
        else:
            messages.info(request, '编辑失败！未做任何修改！')
            return redirect(reverse('account_edit', args=[id, ]))
    return render(request, 'account/edit.html', context={
        'account': account,
        'roles': roles
    })
    pass


@is_login
def pwd(request, id):
    url = URL + 'account/pwd/'
    data = {'id': id}
    res = requests.get(url, params=data)
    account = json.loads(res.text)['account']
    if request.method == 'POST':
        old_pwd = request.POST['old_pwd']
        if not check_password(old_pwd, account['password']):
            messages.info(request, "旧密码错误！")
            return redirect(reverse('account_pwd', kwargs={'id': id}))
        else:
            pwd = request.POST['new_pwd']
            data = {'id': id, 'password': pwd}
            res = requests.post(url, data)
            if account['name'] == request.session.get("user", None):
                return redirect(reverse('account_login'))
            else:
                return redirect(reverse('account_list'))

    return render(request, 'account/pwd.html', context={
        'account': account,
    })

def login(request):
    if request.method == 'POST':
        name = request.POST['username']
        password = request.POST['password']
        # password=make_password(password)
        # remember = request.POST.getlist('remember')
        # print(name, password, remember)
        url = URL + 'account/login/'
        data = {'name': name, 'password': password}
        res = requests.post(url, data=data)
        res = json.loads(res.text)
        if res['status'] == 'ok':
            request.session['user'] = name
            request.session['user_id'] = res['id']

            request.session.set_expiry(60 * 60)
            # if remember:
            #     print('222222222222222')
            #     request.session.set_expiry(60 *2)
            # else:
            #     print('222222222222222')
            return redirect(reverse('music_list'))
        else:

            messages.info(request, res['info'])
            return redirect(reverse('account_login'))
    return render(request, 'account/login.html')

def logout(request):
    del request.session['user']
    del request.session['user_id']
    return redirect(reverse('account_login'))

def name(request):
    if request.method=='POST':
        new_name = request.POST['name']
        id=request.session.get('user_id')
        old_name=request.session.get('user')
        if new_name==old_name:
            messages.info(request, '编辑失败！未做任何修改！')
            return redirect(reverse('account_name'))
        else:
            data = {'id': id, 'name': new_name}
            url = URL + 'account/name/'

            res = requests.post(url, data=data)

            res = json.loads(res.text)
            if res['status'] == 'ok':
                request.session['user'] = new_name
                return redirect(reverse('account_list'))
            else:
                messages.info(request, res['info'])
                return redirect(reverse('account_name'))
    return render(request,'account/name.html')
