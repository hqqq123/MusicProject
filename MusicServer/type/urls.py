from django.urls import path
from type.views import list, add, edit, delete

urlpatterns=[
    path('list/', list,name='type_list'),
    path('add/', add, name='type_add'),
    path('edit/', edit, name='type_edit'),
    path('delete/', delete, name='type_delete'),

]