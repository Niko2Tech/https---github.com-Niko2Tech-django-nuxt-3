from django.urls import include, path
from rest_framework import routers
from .views import *

# router de rest_framework
routers = routers.DefaultRouter()
routers.register("api/user", UserViewSet, "user")
routers.register("api/menu", MenuViewSet, "menu")

urlpatterns = routers.urls
