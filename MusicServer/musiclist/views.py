import json

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from MusicServer.settings import URL
from account.models import Account
from music.models import Music
from musiclist.models import Musiclist


@csrf_exempt
def list(request):
    account_id=request.POST['account_id']
    account=Account.objects.filter(id=account_id).first()
    data = {'musiclists': []}
    if account.role.name=='超级用户':
        # print('-=-=-=')
        musiclists=Musiclist.objects.all()
    else:
        # print('121212')
        if account.musiclist_set:
            musiclists = account.musiclist_set.all()
        else:
            return JsonResponse(data)
    for musiclist in musiclists:
        print(musiclist.account)
        info={'id': musiclist.id, 'name': musiclist.name, 'account_id': musiclist.account.id,
                                   'account_name': musiclist.account.name,'musics':[],'musics_len':len(musiclist.musics.all())}
        for music in musiclist.musics.all():
            musicinfo={'id':music.id,'name':music.name,'type': music.type.name, 'img': URL + music.img,
                'file': URL + music.file, 'singers': []}
            for singer in music.singers.all():
                musicinfo['singers'].append(singer.name)
            info['musics'].append(musicinfo)

        data['musiclists'].append(info)
    print(data)
    return JsonResponse(data)
@csrf_exempt
def musics(request):
    musiclist_name=request.POST['musiclist_name']
    musiclist_account_name=request.POST['musiclist_account_name']
    # account_id=request.POST['account_id']
    account=Account.objects.filter(name=musiclist_account_name).first()

    musiclist=account.musiclist_set.filter(name=musiclist_name).first()
    print(musiclist.musics.all())
    data = {'musics': []}
    for music in musiclist.musics.all():
        musicinfo = {'id': music.id, 'name': music.name, 'type': music.type.name, 'img': URL + music.img,
                     'file': URL + music.file, 'singers': []}
        for singer in music.singers.all():
            musicinfo['singers'].append(singer.name)
        data['musics'].append(musicinfo)
    # print(data)
    return JsonResponse(data)


@csrf_exempt
def edit(request):
    name=request.POST['name']
    id=request.POST['account_id']
    account=get_object_or_404(Account,id=id)
    id=request.POST['id']
    if account.musiclist_set.filter(name=name).first():
        return JsonResponse({'status': 'ok', 'info': '修改失败,歌单已存在'})
    else:
        musiclist=account.musiclist_set.filter(id=id).first()
        musiclist.name=name
        musiclist.save()

        return JsonResponse({'status': 'ok', 'info': '成功'})


@csrf_exempt
def collect(request):
    # collect=Musiclist.objects.filter(name='我收藏的')
    collect=get_object_or_404(Musiclist,name='我收藏的')
    music_id=request.POST['music_id']
    # if int(music_id) in collect
    collect.musics.add(int(music_id))
    collect.save()
    return JsonResponse({'status':'ok','info':'成功'})
@csrf_exempt
def add(request):

    # print('------------*****************')

    # print(request.body.decode())
    # print('==============================')
    # print(type(request.body))
    # print(type(json.loads(request.body)))
    # id=request.GET.get('account_id')
    # print(id)

    if request.method=='GET':
        musics=Music.objects.all()
        data={'musics':[]}
        for music in musics:
            data['musics'].append({'id':music.id,'name':music.name})
        return JsonResponse(data)
    else:
        name=request.POST['name']
        id=request.POST['account_id']
        # name="热死了"
        account=get_object_or_404(Account,id=id)
        # account.musiclist_set
        if account.musiclist_set.filter(name=name).first():
            return JsonResponse({'status': 'no', 'info': '添加失败,歌单已存在'})
        else:
            musiclist=Musiclist(name=name,account=account)
            musiclist.save()
            musics=request.POST.getlist('musics')
            for music_id in musics:
                musiclist.musics.add(int(music_id))
            musiclist.save()
            return JsonResponse({'status':'ok','info':'成功'})

@csrf_exempt
def add_music(request):
    # if request.method=='GET':
    name=request.POST['musiclist_name']

    music_id=request.POST['music_id']
    # music_id=10
    account_id=request.POST['account_id']
    # account_id=1


    account=get_object_or_404(Account,id=account_id)
    musiclist=account.musiclist_set.filter(name=name).first()
    # for music_id in musics_id:
    # if music_id in musiclist.musics.all():
    #     return JsonResponse({'status': 'ok', 'info': '添加失败,该歌曲在此歌单中已存在'})
    # else:
    musiclist.musics.add(int(music_id))
    musiclist.save()
    return JsonResponse({'status': 'ok', 'info': '成功'})
@csrf_exempt
def delete_musics(request):
    music_id = request.POST['id']
    musiclist_name=request.POST['name']

    # account_id = request.POST['account_id']
    account_id = request.POST['account_id']

    print(account_id)
    account = get_object_or_404(Account, id=account_id)
    musiclist = account.musiclist_set.filter(name=musiclist_name).first()
    musiclist.musics.remove(int(music_id))
    musiclist.save()
    return JsonResponse({'status': 'ok', 'info': '成功'})


@csrf_exempt
def delete(request):
    id=request.POST['id']
    # print(id)
    account_id=request.POST['account_id']

    account=get_object_or_404(Account,id=account_id)
    if account.role.name=='普通用户':
        # print('--------11111111111')
        musiclist=account.musiclist_set.filter(id=id).first()
    else:
        # print('22222222222222')
        musiclist=Musiclist.objects.filter(id=id).first()
    musiclist.delete()
    return JsonResponse({'status': 'ok', 'info': '成功'})

@csrf_exempt
def list_android(request):
    account=Account.objects.filter(name='root').first()
    musiclists = account.musiclist_set.all()
    data={'musiclists':[]}
    for musiclist in musiclists:
        info={'id': musiclist.id, 'name': musiclist.name, 'account_id': musiclist.account.id,
                                   'account_name': musiclist.account.name,'musics':[],'musics_len':len(musiclist.musics.all())}
        for music in musiclist.musics.all():
            musicinfo={'id':music.id,'name':music.name,'type': music.type.name, 'img': URL + music.img,
                'file': URL + music.file, 'singers': []}
            for singer in music.singers.all():
                musicinfo['singers'].append(singer.name)
            info['musics'].append(musicinfo)

        data['musiclists'].append(info)
    # print(data)
    return JsonResponse(data)

@csrf_exempt
def list_rec(request):
    account=Account.objects.filter(name='hq').first()
    musiclists = account.musiclist_set.all()
    data={'musiclists':[]}
    for musiclist in musiclists:
        info={'id': musiclist.id, 'name': musiclist.name, 'account_id': musiclist.account.id,
                                   'account_name': musiclist.account.name,'musics':[],'musics_len':len(musiclist.musics.all())}
        for music in musiclist.musics.all():
            musicinfo={'id':music.id,'name':music.name,'type': music.type.name, 'img': URL + music.img,
                'file': URL + music.file, 'singers': []}
            for singer in music.singers.all():
                musicinfo['singers'].append(singer.name)
            info['musics'].append(musicinfo)

        data['musiclists'].append(info)
    print(data)
    return JsonResponse(data)