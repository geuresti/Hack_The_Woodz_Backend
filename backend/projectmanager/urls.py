from django.urls import path
from .views import ProjectViewSet, UserViewSet
from rest_framework.authtoken import views
from django.contrib.auth import views as auth

urlpatterns = [
    path('projects/', ProjectViewSet.as_view({'get':'projects'})),
    path('create/', ProjectViewSet.as_view({'post':'create'})),
    path('update/', ProjectViewSet.as_view({'post':'update'})),
    path('get_image/', ProjectViewSet.as_view({'get':'get_image'})),
    path('auth_token/', views.obtain_auth_token, name='auth_token'),
    #path('log_in/', UserViewSet.as_view({'get':'log_in'})),
]
