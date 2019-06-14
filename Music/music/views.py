import json
import os
from datetime import datetime

import requests
from django.contrib import messages
from django.core import paginator
from django.core.paginator import Paginator
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse

from Music.settings import URL, MUSIC_IMG_DIR, MUSIC_FILE_DIR
from account.views import is_login, is_auth


def change_filename(filename):
    return datetime.now().strftime('%Y%m%d_%H%M%S') + '_' + filename


@is_login
@is_auth
def add(request):
    print('------------')
    url = URL + 'music/add/'
    res = requests.get(url=url)
    data = json.loads(res.text)
    singers = data['singers']
    types = data['types']
    if request.method == 'POST':
        name = request.POST['name']
        singers_id = request.POST.getlist('singers')
        type_id = request.POST['type']
        img = request.FILES.get('img', None)
        file = request.FILES.get('file', None)
        # print(img.name,'--',singers_id)
        data = {
            'name': name,
            'singers_id': singers_id,
            'type_id': type_id,
        }
        files = {}
        if img:
            img_path = MUSIC_IMG_DIR
            if not os.path.exists(img_path):
                os.makedirs(img_path)

            print(img_path)
            img_name = change_filename(img.name)

            with open(img_path + img_name, 'wb') as f:
                for chunk in img.chunks():
                    f.write(chunk)
            # data['img']=[img_name, open(img_path+img_name,'rb').read()]
            files['img'] = open(img_path + img_name, 'rb')
            # files['img']=(img_name,open(img_path+img_name,'rb'))

        else:
            # data['img']=None
            files['img'] = None
        if file:
            file_path = MUSIC_FILE_DIR

            if not os.path.exists(file_path):
                os.makedirs(file_path)

            file_name = change_filename(file.name)
            with open(file_path + file_name, 'wb') as f:
                for chunk in file.chunks():
                    f.write(chunk)
            files['file'] = open(file_path + file_name, 'rb')

        else:
            files['file'] = None
        # print(data)
        # print(files)
        res = requests.post(url=url, data=data, files=files)
        res = json.loads(res.text)
        if res['status'] == 'ok':
            return redirect(reverse('music_list'))
        else:
            messages.info(request, res['info'])
            return redirect(reverse('music_add'))
    return render(request, 'music/add.html', context={
        'singers': singers,
        'types': types,
    })


@is_login
def list(request):
    url = URL + 'music/list/'
    account_id = request.session.get('user_id')
    print(account_id)
    data = {'id': account_id}
    res = requests.get(url=url, params=data)
    # print(res.text)
    # print(res.headers,'------------------------')

    data = json.loads(res.text)
    musics = data['musics']
    musiclists = data['musiclists']

    PageObj = Paginator(musics, per_page=5)
    page = request.GET.get('page', 1)
    musicsPageObj = PageObj.page(page)
    musics = musicsPageObj.object_list
    return render(request, 'music/list.html', context={
        'musics': musics,
        'musiclists': musiclists,
        'musicsPageObj': musicsPageObj,
    })


@is_login
@is_auth
def delete(request, id):
    url = URL + 'music/delete/'
    data = {'id': id}
    res = requests.post(url=url, data=data)
    return redirect(reverse('music_list'))


@is_login
@is_auth
def edit(request, id):
    url = URL + 'music/edit/'
    res = requests.get(url, params={'id': id})
    data = json.loads(res.text)
    music = data['music']
    # print(music.name)
    singers = data['singers']
    types = data['types']
    if request.method == 'POST':
        print('-----------------------------')
        name = request.POST['name']
        singers_id = request.POST.getlist('singers')
        type = request.POST['type']
        img = request.FILES.get('img', None)
        file = request.FILES.get('file', None)
        print(file)
        print(img)
        # print(music['img'] == URL, music['img'].split('_')[-1])
        # # print(img.name)
        # print(img is None, img.name == music['img'].split('_')[-1])
        singers = []
        for id in singers_id:
            singers.append(int(id))
        if name == music['name'] and singers == music['singers'] and int(type) == music['type'] and (
                img is None or img.name == music['img'].split('_')[-1]) and (
                file is None or file.name == music['file'].split('_')[-1]):

            messages.info(request, '未做任何修改')
            return redirect(reverse('music_edit', kwargs={'id': music['id']}))
        else:
            data = {}
            files = {}
            if name != music['name']:
                data['name'] = name
            else:
                data['name'] = music['name']
            if singers != music['singers']:
                data['singers'] = singers
            else:
                data['singers'] = music['singers']
            if int(type) != music['type']:
                data['type'] = int(type)
            else:
                data['type'] = music['type']
            if img is not None and img.name != music['img'].split('_')[-1]:
                img_path = MUSIC_IMG_DIR
                if not os.path.exists(img_path):
                    os.makedirs(img_path)

                print(img_path)
                img_name = change_filename(img.name)

                with open(img_path + img_name, 'wb') as f:
                    for chunk in img.chunks():
                        f.write(chunk)

                files['img'] = open(img_path + img_name, 'rb')
            else:
                data['img'] = music['img']
                # print(files['img'],'****************')

            if file is not None and file.name != music['file'].split('_')[-1]:
                file_path = MUSIC_FILE_DIR

                if not os.path.exists(file_path):
                    os.makedirs(file_path)

                file_name = change_filename(file.name)
                with open(file_path + file_name, 'wb') as f:
                    for chunk in img.chunks():
                        f.write(chunk)
                files['file'] = open(file_path + file_name, 'rb')
            else:
                data['file'] = music['file']
            res = requests.post(url=url, data=data, files=files)

            res = json.loads(res.text)
            print(res)
            if res['status'] == 'ok':
                return redirect(reverse('music_list'))
            else:
                messages.info(request, res['info'])
                return redirect(reverse('music_edit', kwargs={'id': music['id']}))

    return render(request, 'music/edit.html', context={
        'music': music,
        'singers': singers,
        'types': types,
    })

def search(request):
    name=request.GET.get('name')

    account_id = request.session.get('user_id')
    data = {'id': account_id,'name':name}
    url=URL+'music/search/'
    res = requests.get(url=url, params=data)

    data = json.loads(res.text)
    musics = data['musics']
    musiclists = data['musiclists']

    PageObj = Paginator(musics, per_page=5)
    page = request.GET.get('page', 1)
    musicsPageObj = PageObj.page(page)
    musics = musicsPageObj.object_list
    return render(request, 'music/list.html', context={
        'musics': musics,
        'musiclists': musiclists,
        'musicsPageObj': musicsPageObj,
    })


def test(request):
    url = 'http://192.168.43.133:8080/' + 'Music_Player/HelloWorld?method="insert"'
    data = {'id': 1}
    res = requests.get(url=url, params=data)
    print(res.text)
    # musics=json.loads(res.text)['musics']
    # return render(request,'music/list.html',context={
    #     'musics':musics,
    # })
