from django.urls import path

from account.views import add, list, edit, delete, pwd, login, auths, name

urlpatterns = [
    path('list/', list, name='account_list'),
    path('add/', add, name='account_add'),
    path('edit/', edit, name='account_edit'),
    path('delete/', delete, name='account_delete'),
    path('pwd/', pwd, name='account_pwd'),
    path('login/', login, name='account_login'),
    path('auths/', auths, name='account_auths'),
    path('name/', name, name='account_name'),

]