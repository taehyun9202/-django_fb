from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path("", views.main),
    path("register", views.register),
    path("login", views.login),
    path("home",views.home),
    path('logout', views.logout),
    path('edit', views.edit),
    path('update', views.update),
    path('user/<userid>',views.timeline),
    path('user/<userid>/friends',views.userfriends),
    path('user/<userid>/update', views.updateinfo),
    path('user/<userid>/photos', views.photos),
    path('post', views.post),
    path('post/<postid>', views.showpost),
    path("addfriend", views.addfriend),
    path('reply', views.reply),
    path('changephoto', views.changephoto),
    path('changecover', views.changecover),
    path("search", views.search),
    path("search/<searchtext>", views.searchbyname),
    path("deletepost", views.deletepost),
    path("deletecomment", views.deletecomment),
    path("unfriend", views.unfriend),
    path('sendemail', views.sendemail),
    path('contact', views.contact),
]
