from django.urls import path
from music.views import add,list,delete,edit, search, list_android
urlpatterns=[
    path('add/',add,name="music_add"),
    path('list/', list, name="music_list"),
    path('songlist/', list_android, name="music_list_android"),

    path('delete/', delete, name="music_delete"),
    path('edit/', edit, name="music_edit"),
    path('search/', search, name="search"),

]