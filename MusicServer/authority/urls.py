from django.urls import path
from authority.views import add, list, delete, edit

urlpatterns = [
    path('add/', add, name="authority_add"),
    path('list/', list, name="authority_list"),
    path('delete/', delete, name="authority_delete"),
    path('edit/', edit, name="authority_edit"),

]
