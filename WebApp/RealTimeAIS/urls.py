"""RealTimeAIS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from main import views
from .db_connection import open_tunnel


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('latest', views.latest),  # Latest gets all points and sends them along to the front end
    path('region/<str:points>', views.region),  # update gets all points within the region sending them to the front end
    path('search/<str:criteria>/', views.search),   # search searches the leveldb database
    path('raw/latest', views.raw_latest),  # newest gets all points and sends them back only as a json response
    path('raw/region/<str:points>', views.raw_region),  # update returns all points within the region as a response
    path('raw/search/<str:criteria>/', views.search)   # search searches the leveldb database and does not update the map
]

#open_tunnel()
