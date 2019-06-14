from django.urls import path

from authority.views import add, list, edit, delete

urlpatterns = [
    path('list/', list, name='authority_list'),
    path('add/', add, name='authority_add'),
    path('edit/<int:id>/', edit, name='authority_edit'),
    path('delete/<int:id>/', delete, name='authority_delete'),
]