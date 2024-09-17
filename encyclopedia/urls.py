from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>",views.get_content,name="wiki"),
    path("wiki/",views.search, name="search"),
    path("add",views.add,name="add"),
    path("random",views.randomContent,name="random"),
    path("wiki/edit/<str:title>",views.editEntry, name="edit")
]
