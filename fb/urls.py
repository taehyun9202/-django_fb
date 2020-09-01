"""fb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.contrib import admin
from fbApp.models import *
from django.conf.urls.static import static
from django.conf import settings

class UserAdmin(admin.ModelAdmin):
    list_display = ['firstName', 'lastName', 'email' , 'created_at']
    search_fields = ['firstName', 'lastName', 'email']
    pass
admin.site.register(User, UserAdmin)

class PostAdmin(admin.ModelAdmin):
    list_display = ['content', 'p_creater', 'p_to', 'created_at']
    search_fields = ['content']
    pass
admin.site.register(Post, PostAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = ['content', 'c_creater', 'c_message', 'created_at']
    search_fields = ['content']
    pass
admin.site.register(Comment, CommentAdmin)

class FriendAdmin(admin.ModelAdmin):
    list_display = ['creater', 'flist', 'created_at']
    search_fields = ['creater', 'flist']
    pass
admin.site.register(Friend, FriendAdmin)


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("fbApp.urls"))
]

# routes to serve up media and static files, do something else in production
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)