import json

import requests
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse

from Music.settings import URL


# 歌单列表
from account.views import is_auth, is_login


@is_login
@is_auth
def list(request):
    url = URL + 'musiclist/list/'
    account_id = request.session.get('user_id')

    res = requests.post(url, data={'account_id': account_id})
    musiclists = json.loads(res.text)['musiclists']
    # print(musiclists)
    PageObj = Paginator(musiclists, per_page=5)
    page = request.GET.get('page', 1)
    musiclistsPageObj = PageObj.page(page)
    musiclists = musiclistsPageObj.object_list
    return render(request, 'musiclist/list.html', context={
        'musiclists': musiclists,
        'musiclistsPageObj': musiclistsPageObj,
    })


# 歌单的歌曲列表
@is_login
@is_auth
def music_list(request):
    account_id = request.session.get('user_id')
    name = request.GET.get('name')
    musiclist_account_name = request.GET.get('musiclist_account_name')
    musiclist_account_id=request.GET.get('musiclist_account_id')

    musiclist_name = name
    url = URL + 'musiclist/musics/'

    # print(musiclist_name)
    res = requests.post(url, data={'musiclist_account_name': musiclist_account_name, 'musiclist_name': musiclist_name,
                                   'account_id': account_id})
    musics = json.loads(res.text)['musics']
    PageObj=Paginator(musics,per_page=5)
    page=request.GET.get('page',1)
    musicsPageObj=PageObj.page(page)
    musics=musicsPageObj.object_list
    return render(request, 'musiclist/musics.html', context={
        'musics': musics,
        'musicsPageObj':musicsPageObj,
        'musiclist_name': musiclist_name,
        'musiclist_account_name':musiclist_account_name,
        'musiclist_account_id':musiclist_account_id,
    })


# 添加歌单
@is_login
@is_auth
def add(request):
    url = URL + 'musiclist/add/'
    res = requests.get(url)
    musics = json.loads(res.text)['musics']
    if request.method == 'POST':
        account_id = request.session['user_id']
        # print(account_id)
        name = request.POST['name']
        musics = request.POST.getlist('musics')

        # print(musics)
        res = requests.post(url, data={'name': name, 'musics': musics, 'account_id': account_id})
        res = json.loads(res.text)
        if res['status'] == 'ok':
            return redirect(reverse('musiclist_list'))
        else:
            messages.info(request, res['info'])
            return redirect(reverse('musiclist_add'))

    return render(request, 'musiclist/add.html', context={
        'musics': musics,
    })

@is_login
def add_music(request, id):
    account_id = request.session.get('user_id')
    musiclist_name = request.GET.get('musiclist_name')
    url = URL + 'musiclist/music/add/'
    data = {'music_id': id, 'account_id': account_id, 'musiclist_name': musiclist_name}
    res = requests.post(url, data=data)
    return redirect(reverse('music_list'))

@is_login
@is_auth
def edit(request, id):
    if request.method == 'POST':
        url = URL + 'musiclist/edit/'
        account_id = request.session.get('user_id')
        name = request.POST['name']
        res = requests.post(url, data={'account_id': account_id, 'name': name, 'id': id})
        res = json.loads(res.text)
        if res['status'] == 'ok':
            return redirect(reverse('musiclist_list'))
        else:
            messages.info(request, res['info'])
            return redirect(reverse('musiclist_edit', kwargs={'id': id}))
    musiclist_name = request.GET.get('musiclist_name')

    return render(request, 'musiclist/edit.html', context={
        'musiclist_name': musiclist_name,
        'musiclist_id': id,
    })

@is_login
@is_auth
def delete(request, id):
    url = URL + 'musiclist/delete/'
    account_id = request.session.get('user_id')
    # print(id,'============')
    res = requests.post(url, data={'account_id': account_id, 'id': id})

    return redirect(reverse('musiclist_list'))

@is_login
# @is_auth
def delete_music(request, id):
    url = URL + 'musiclist/music/delete/'
    name = request.GET.get('name')#歌单,id 是音乐的
    musiclist_account_name = request.GET.get('musiclist_account_name')
    account_id=request.GET.get('musiclist_account_id')
    print(account_id)
    res = requests.post(url, data={'id': id, 'name': name,'account_id':account_id})
    return redirect(reverse('musiclist_musics') + '?name=' + name+'&musiclist_account_name='+musiclist_account_name)
