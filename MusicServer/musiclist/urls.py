from django.urls import path

from musiclist.views import add, list, edit, delete, add_music, collect, delete_musics, musics,list_android, list_rec

urlpatterns = [
    path('list/', list, name='musiclist_list'),
    path('android/list/', list_android, name='musiclist_list_android'),
    path('rec/list/', list_rec, name='musiclist_list_android'),

    path('add/', add, name='musiclist_add'),
    path('music/add/', add_music, name='musiclist_add_music'),
    path('musics/', musics, name='musiclist_musics'),

    path('collect/', collect, name='musiclist_collect'),
    path('edit/', edit, name='musiclist_edit'),
    path('delete/', delete, name='musiclist_delete'),
    path('music/delete/', delete_musics, name='musiclist_delete_musics'),

]