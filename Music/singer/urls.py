from django.urls import path

from singer.views import base, list, add, edit, delete

urlpatterns = [
    path('', base, name='base'),
    path('list/', list, name='singer_list'),
    path('add/', add, name='singer_add'),
    path('edit/<int:id>/', edit, name='singer_edit'),
    path('delete/<int:id>/', delete, name='singer_delete'),

    # path('list/', list, name='account_list'),
    # path('add/', add, name='account_add'),
    # path('edit/<int:id>/', edit, name='account_edit'),
    # path('delete/<int:id>/', delete, name='account_delete'),
    # path('pwd/', pwd, name='account_pwd'),

]