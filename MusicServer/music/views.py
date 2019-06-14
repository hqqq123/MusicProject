import os
from datetime import datetime

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from MusicServer.settings import MUSIC_IMG_DIR, MUSIC_FILE_DIR, MUSIC_IMG_URL, MUSIC_FILE_URL, URL
from account.models import Account
from music.models import Music
from musiclist.models import Musiclist
from singer.models import Singer
from type.models import Type


def change_filename(filename):
    return datetime.now().strftime('%Y%m%d_%H%M%S') + '_' + filename


@csrf_exempt
def add(request):
    if request.method == 'GET':
        singers = Singer.objects.all()
        types = Type.objects.all()
        singers_li = []
        for singer in singers:
            singers_li.append({'id': singer.id, 'name': singer.name})
        types_li = []
        for type in types:
            types_li.append({'id': type.id, 'name': type.name})

        data = {'singers': singers_li, 'types': types_li}
        return JsonResponse(data)
    else:
        name = request.POST['name']
        singers_id = request.POST.getlist('singers_id')
        # print(singers_id, '-----------')
        music = Music.objects.filter(name=name).first()

        is_exit = True
        if music is not None:
            # print(music.singers.all())
            if len(singers_id) == len(music.singers.all()):
                for singer in music.singers.all():
                    if str(singer.id) not in singers_id:
                        is_exit = False
                        break
            else:
                is_exit = False
        else:
            is_exit = False

        if is_exit is True:
            data = {'status': 'no', 'info': '添加歌曲失败，歌曲已存在'}
            return JsonResponse(data)
        else:
            type_id = request.POST['type_id']
            img = request.FILES.get('img')
            file = request.FILES.get('file')

            if img is not None:
                # print(img.name, '==============')
                img_path = MUSIC_IMG_DIR
                if not os.path.exists(img_path):
                    os.makedirs(img_path)


                with open(img_path + img.name, 'wb') as f:

                    for chunk in img.chunks():
                        f.write(chunk)

                imgPath = MUSIC_IMG_URL + img.name
            else:
                imgPath = ''
            if file is not None:

                file_path = MUSIC_FILE_DIR
                if not os.path.exists(file_path):
                    os.makedirs(file_path)
                # file_name=change_filename(file.name)
                with open(file_path + file.name, 'wb') as f:
                    for chunk in file.chunks():
                        f.write(chunk)
                filePath = MUSIC_FILE_URL + file.name
            else:
                filePath = ''
            # print(type_id)
            typeObj = get_object_or_404(Type, id=type_id)
            music = Music(name=name, img=imgPath, file=filePath, type=typeObj)
            music.save()

            for id in singers_id:
                music.singers.add(int(id))
            music.save()

            data = {'status': 'ok', 'info': '添加歌曲成功'}
            return JsonResponse(data)


def list(request):
    # print(request.GET.get('name'))
    account_id=request.GET.get('id')
    account=Account.objects.filter(id=account_id).first()
    musics = Music.objects.all()
    data = {'musics': [],'musiclists':[]}
    for music in musics:

        info = {'type': music.type.name, 'id': music.id, 'img': URL + music.img, 'name': music.name,
                'file': URL + music.file, 'singers': []}
        for singer in music.singers.all():
            info['singers'].append(singer.name)
        data['musics'].append(info)
    # print(data)
    musiclists=account.musiclist_set.all()
    for musiclist in musiclists:
        info = {'id': musiclist.id, 'name': musiclist.name,
                'musics': []}
        for music in musiclist.musics.all():
            # info['musics'].append({'id':music.id,'name':music.name})
            info['musics'].append(music.name)

        data['musiclists'].append(info)

    return JsonResponse(data)

def list_android(request):
    # print(request.GET.get('name'))
    account_id=request.GET.get('id')
    # account=Account.objects.filter(id=account_id).first()
    musics = Music.objects.all()
    data = {'musics': []}
    for music in musics:

        info = {'type': music.type.name, 'id': music.id, 'img': URL + music.img, 'name': music.name,
                'file': URL + music.file, 'singers': []}
        for singer in music.singers.all():
            info['singers'].append(singer.name)
        data['musics'].append(info)
    # print(data)
    # musiclists=account.musiclist_set.all()
    # for musiclist in musiclists:
    #     info = {'id': musiclist.id, 'name': musiclist.name,
    #             'musics': []}
    #     for music in musiclist.musics.all():
    #         # info['musics'].append({'id':music.id,'name':music.name})
    #         info['musics'].append(music.name)
    #
    #     data['musiclists'].append(info)

    return JsonResponse(data)

@csrf_exempt
def delete(request):
    print(request.body)

    id = request.POST['id']
    music = get_object_or_404(Music, id=id)
    music.delete()
    data = {'status': 'ok', 'info': '成功'}
    return JsonResponse(data=data)


@csrf_exempt
def edit(request):
    if request.method == 'GET':

        print(request.body,'*******************')

        id = request.GET.get('id')
        music = get_object_or_404(Music, id=id)
        data = {'id': id, 'name': music.name, 'type': music.type.id, 'img': URL + music.img,
                'file': URL + music.file, 'singers': []}
        for singer in music.singers.all():
            data['singers'].append(singer.id)

        singers = Singer.objects.all()
        types = Type.objects.all()
        singers_li = []
        for singer in singers:
            singers_li.append({'id': singer.id, 'name': singer.name})
        types_li = []
        for type in types:
            types_li.append({'id': type.id, 'name': type.name})

        data = {'music': data, 'singers': singers_li, 'types': types_li}
        return JsonResponse(data)
    else:
        name = request.POST['name']
        singers_id = request.POST.getlist('singers')
        print(singers_id, '-----------')
        music = Music.objects.filter(name=name).first()
        is_exit = True
        if music is not None:
            print(music.singers.all())
            if len(singers_id) == len(music.singers.all()):
                for singer in music.singers.all():
                    if singer.id not in singers_id:
                        is_exit = False
                        break
            else:
                is_exit = False
        else:
            is_exit = False
        if is_exit is True:
            data = {'status': 'no', 'info': '添加歌曲失败，歌曲已存在'}
            return JsonResponse(data)
        else:
            type_id = request.POST['type']
            img = request.FILES.get('img')
            file = request.FILES.get('file')
            # print(img,i)
            # try:
            #     img_name=img.name
            #     print(img.name)
            #
            # except:
            #     imgPath=img
            #     print(imgPath)
            # else:
            if img is not None:
                print(img.name, '==============')
                img_path = MUSIC_IMG_DIR
                if not os.path.exists(img_path):
                    os.makedirs(img_path)

                # img_name = change_filename(img.name)

                with open(img_path + img.name, 'wb') as f:
                    for chunk in img.chunks():
                        f.write(chunk)
                imgPath = MUSIC_IMG_URL + img.name
            else:
                img = request.POST['img']

                imgPath = music.img
            if file is not None:

                file_path = MUSIC_FILE_DIR
                if not os.path.exists(file_path):
                    os.makedirs(file_path)
                file_name = change_filename(file.name)
                with open(file_path + file_name, 'wb') as f:
                    for chunk in img.chunks():
                        f.write(chunk)
                filePath = MUSIC_FILE_URL + file_name
            else:
                file = request.POST['file']
                filePath = music.file
            # print(type_id)
            typeObj = get_object_or_404(Type, id=type_id)
            music.name = name
            music.img = imgPath
            music.file = filePath
            music.type = typeObj
            music.singers.clear()
            for id in singers_id:
                music.singers.add(int(id))
            music.save()

            data = {'status': 'ok', 'info': '添加歌曲成功'}
            return JsonResponse(data)

@csrf_exempt
def search(request):
    account_id = request.GET.get('id')
    account = Account.objects.filter(id=account_id).first()

    name=request.GET.get('name')
    musics=Music.objects.filter(name__contains=name).all()

    data = {'musics': [], 'musiclists': []}
    for music in musics:

        info = {'type': music.type.name, 'id': music.id, 'img': URL + music.img, 'name': music.name,
                'file': URL + music.file, 'singers': []}
        for singer in music.singers.all():
            info['singers'].append(singer.name)
        data['musics'].append(info)
    # print(data)
    musiclists = account.musiclist_set.all()
    for musiclist in musiclists:
        info = {'id': musiclist.id, 'name': musiclist.name,
                'musics': []}
        for music in musiclist.musics.all():
            # info['musics'].append({'id':music.id,'name':music.name})
            info['musics'].append(music.name)

        data['musiclists'].append(info)

    return JsonResponse(data)