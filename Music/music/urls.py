from django.urls import path
from music.views import add, list, delete, edit, test, search

urlpatterns = [
    path('add/', add, name='music_add'),
    path('list/', list, name='music_list'),
    path('delete/<int:id>/', delete, name='music_delete'),
    path('edit/<int:id>/', edit, name='music_edit'),
    path('search/', search, name="search"),

    path('test/', test, name="test"),
    # path('', list, name='index'),

]
