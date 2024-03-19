"""catalogo URL Configuration

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
from ast import pattern
from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path
from django.contrib.auth import views as auth_views
from bot.views import catalogo, manual,senales,senales2,buy_senales, get_info, login_view,get_respuestas, historial, clear_historial, operaciones, buy_sell, foro, conectar, conectar2, porcentaje, stop, respuesta, voto, resultados, index, bienvenida,salir

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", index, name='index'),
    path("senales", senales, name='senales'),
    path("senales2", senales2, name='senales2'),
    path("buy_senales", buy_senales, name='buy_senales'),
    path("manual/", manual, name='manual'),
    path("logout", salir),
    path("registered", bienvenida, name="bienvenida"),
    path("login-page",login_view, name="login"),
    #path('change_password/', auth_views.PasswordResetView.as_view(), name='change_password'),
    #path('password_change_done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('password_reset_confirm/<slug:uidb64>/<slug:token>/', auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
  
    path("foro/<str:filtro>", foro, name='foro'),
    path("foro/respuesta/",respuesta),
    path("foro/voto/",voto),
    path("historial",historial, name='historial'),
    path("clear_historial",clear_historial, name='clear_historial'),
    path("foro/get_info/",get_info),
    path("foro/get_respuestas/",get_respuestas),
    path("catalogo/<str:plan>", catalogo, name='catalogo'),
    path("catalogo/operaciones/",operaciones),
    path("catalogo/conectar/",conectar),
    path("catalogo/conectar2/",conectar2),
    path("catalogo/buy_sell/",buy_sell),
    path("catalogo/porcentaje/",porcentaje),
    path("catalogo/resultados/",resultados),
    path("catalogo/stop/",stop),
]

