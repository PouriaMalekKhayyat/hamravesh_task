"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from project.views import app_views, run_views

urlpatterns = [
    path('apps/', app_views.app_list),
    path('apps/build/', app_views.app_build),
    path('apps/<int:id>/', app_views.app_detail),
    path('apps/<int:id>/run/', app_views.app_run),
    path('apps/<int:id>/history/', run_views.run_list),
    path('runs/<int:id>/status/', run_views.run_status),
    path('admin/', admin.site.urls),
]
