import json

import requests
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse

from Music.settings import URL
from account.views import is_auth, is_login


@is_login
@is_auth
def add(request):
    if request.method == 'POST':
        name = request.POST['name']
        _url = request.POST['url']
        data = {'name': name, 'url': _url}
        url = URL + 'authority/add/'
        res = requests.post(url, data=data)

        res = json.loads(res.text)
        if res['status'] == 'ok':
            return redirect(reverse('authority_list'))
        else:
            messages.info(request, res['info'])
            return redirect(reverse('authority_add'))

    return render(request, 'authority/add.html')

@is_login
@is_auth
def list(request):
    url = URL + 'authority/list/'
    res = requests.get(url)
    authorities = json.loads(res.text)['authorities']

    PageObj = Paginator(authorities, per_page=5)
    page = request.GET.get('page', 1)

    authoritiesPageObj = PageObj.page(page)
    authorities = authoritiesPageObj.object_list

    return render(request, 'authority/list.html', context={
        'authorities': authorities,
        'authoritiesPageObj': authoritiesPageObj,
    })

@is_login
# @is_auth
def edit(request, id):
    name = request.GET.get('name')
    url = request.GET.get('url')
    if request.method == 'POST':
        _name = request.POST['name']
        _url = request.POST['url']
        url = URL + 'authority/edit/'
        res = requests.post(url, data={'id': id, 'name': _name, 'url': _url})
        res = json.loads(res.text)
        if res['status'] == 'ok':
            return redirect(reverse('authority_list'))
        else:
            messages.info(request, res['info'])
            return redirect(reverse('authority_edit', kwargs={'id': id}) + '?name=' + _name + '&url=' + _url)

    return render(request, 'authority/edit.html', context={
        'name': name,
        'url': url,
        'id': id,
    })

@is_login
@is_auth
def delete(request, id):
    url = URL + 'authority/delete/'
    res = requests.post(url, data={'id': id})

    return redirect(reverse('authority_list'))
