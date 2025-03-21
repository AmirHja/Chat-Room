from django.contrib import admin
from django.shortcuts import render
from django.urls import path, include

import computerNetworkProject.views as views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('', views.index_view, name='home'),
]
