from django.urls import path
from role.views import list, add, edit, delete

urlpatterns = [
    path('list/', list, name='role_list'),
    path('add/', add, name='role_add'),
    path('edit/', edit, name='role_edit'),
    path('delete/', delete, name='role_delete'),

]