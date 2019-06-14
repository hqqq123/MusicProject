from django.urls import path

from account.views import add, list, edit, delete, pwd, login, logout, name

urlpatterns = [
    path('list/', list, name='account_list'),
    path('add/', add, name='account_add'),
    path('edit/<int:id>/', edit, name='account_edit'),
    path('delete/<int:id>/', delete, name='account_delete'),
    path('pwd/<int:id>/', pwd, name='account_pwd'),
    path('login/', login, name='account_login'),
    path('logout/', logout, name='account_logout'),
    path('name/', name, name='account_name'),

]