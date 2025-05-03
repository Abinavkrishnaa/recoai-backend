from django.urls import  path,include
from rest_framework.routers import DefaultRouter
from .views import  UserViewSet,ContentViewSet,UserInteractionViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'content', ContentViewSet)
router.register(r'interactions', UserInteractionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]