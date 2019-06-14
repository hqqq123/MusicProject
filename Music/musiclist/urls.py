from django.urls import path
from musiclist.views import add, list, delete, edit, music_list, delete_music, add_music

urlpatterns = [
    path('add/', add, name='musiclist_add'),
    path('list/', list, name='musiclist_list'),
    path('musics/', music_list, name='musiclist_musics'),
    path('music/add/<int:id>/', add_music, name='musiclist_music_add'),

    path('delete/<int:id>/', delete, name='musiclist_delete'),
    path('music/delete/<int:id>/', delete_music, name='musiclist_music_delete'),

    path('edit/<int:id>/', edit, name='musiclist_edit'),
    # path('test/',test,name="test")

]
