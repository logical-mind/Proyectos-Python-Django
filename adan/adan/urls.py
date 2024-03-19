"""adan URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from adanapp.views import index, unete, secciones, secciones_form, post_create,table,eliminar,coordinadores,salir

urlpatterns = [
    path("admin/", admin.site.urls),
    path("home", index),
    path("", unete),
    path("seccion/", secciones),
    path("secciones_form/", secciones_form),
    path("post_create/", post_create),
    path("table/", table),
    path("eliminar/", eliminar),
    path("coordinadores/", coordinadores),
    path("accounts/", include("django.contrib.auth.urls")),
    path("salir/", salir),
    
]
