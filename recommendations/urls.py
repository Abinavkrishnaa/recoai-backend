from django.urls import  path,include
from rest_framework.routers import DefaultRouter
from .views import  UserViewSet,ContentViewSet,UserInteractionViewSet,RegisterView,RecommendationView,CurrentUserView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'content', ContentViewSet)
router.register(r'interactions', UserInteractionViewSet)
urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('recommend/', RecommendationView.as_view(), name='recommend'),
    path('users/me/', CurrentUserView.as_view(), name='current-user'),
]
urlpatterns += [
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]