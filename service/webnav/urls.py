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
from webnav import views
from django.urls import path

urlpatterns = [
    path("api/webnavlabel_get/", views.webnavlabel_get),
    path("api/webnavlabel/webnavlabel_get_single/", views.webnavlabel_get_single),
    path("api/webnavlabel/webnavlabel_upd_single/", views.webnavlabel_upd_single),
    path("api/webnavlabel/webnavlabel_del_single/", views.webnavlabel_del_single),
    path("api/webnavlabel/webnavlabel_add/", views.webnavlabel_add),

    path("api/webnav/", views.webnav),
    path("api/cwebnav/", views.cwebnav_get),
    path("api/cwebnav/cwebnav_get_single/", views.cwebnav_get_single),
    path("api/cwebnav/cwebnav_upd_single/", views.cwebnav_upd_single),
    path("api/cwebnav/cwebnav_del_single/", views.cwebnav_del_single),
    path("api/cwebnav/cwebnav_add/", views.cwebnav_add),
]
