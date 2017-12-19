from django.conf import settings
from django.conf.urls import include, url
from rest_framework import routers

from example.api.views import (
    CarViewSet,
    ManufacturerViewSet,
)

router = routers.DefaultRouter()

router.register(r'cars', CarViewSet)
router.register(r'manufacturers', ManufacturerViewSet)

urlpatterns = [
    url(r'^api/', include(router.urls)),
]
