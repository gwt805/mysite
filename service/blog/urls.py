"""
URL configuration for service project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from blog import views
from django.urls import path

urlpatterns = [
    path("api/blog/getblog_single/", views.get_blog_single),
    path("api/blog/getblog/", views.get_blog),
    path("api/blog/create_blog/", views.create_blog),
    path("api/blog/update_blog/", views.update_blog),
    path("api/blog/delete_blog/", views.delete_blog),
    path("api/blog/uploadimg/", views.uploadimg),
    path("api/blog/uploadother/", views.uploadvideo),
    path("api/blog/getfile/", views.getfile),
    path("api/blog/removefile/", views.removefile),
]
