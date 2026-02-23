from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from cr_backend.views import ChangeRequestViewSet

router = DefaultRouter()
router.register('change-requests', ChangeRequestViewSet, basename='change-request')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
