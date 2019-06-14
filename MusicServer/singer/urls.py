from django.urls import path
from singer.views import list, add, edit, delete

urlpatterns=[
    path('list/',list,name='singer_list'),
    path('add/', add, name='singer_add'),
    path('edit/', edit, name='singer_edit'),
    path('delete/', delete, name='singer_delete'),

]