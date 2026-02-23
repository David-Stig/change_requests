from rest_framework.routers import DefaultRouter

from .views import ChangeRequestViewSet, FunctionalityViewSet, MinistryViewSet, SystemViewSet, UserViewSet

router = DefaultRouter()
router.register(r'ministries', MinistryViewSet, basename='ministry')
router.register(r'systems', SystemViewSet, basename='system')
router.register(r'functionalities', FunctionalityViewSet, basename='functionality')
router.register(r'change-requests', ChangeRequestViewSet, basename='change-request')
router.register(r'users', UserViewSet, basename='user')

urlpatterns = router.urls
