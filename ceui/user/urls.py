from django.urls import include, path
from knox import views as knox_views
from rest_framework.routers import DefaultRouter
from .views import RegisterAPI, LoginAPI, LogoutAPI, UserViewSet
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),  # ViewSet'i API'ye dahil et
    path('register/', RegisterAPI.as_view(), name='register'),
    path('login/', LoginAPI.as_view(), name='login'),
    path('logout/', LogoutAPI.as_view(), name='logout'),
]
