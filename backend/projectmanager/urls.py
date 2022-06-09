from django.urls import path
from .views import ProjectViewSet, UserViewSet
from rest_framework.authtoken import views
from django.contrib.auth import views as auth

urlpatterns = [
    path('projects/', ProjectViewSet.as_view({'get':'projects'})),
    path('create/', ProjectViewSet.as_view({'post':'create'})),
    path('update/', ProjectViewSet.as_view({'post':'update'})),
    path('delete_project/', ProjectViewSet.as_view({'delete':'delete_project'})),
    path('view_project/', ProjectViewSet.as_view({'get':'view_project'})),
    path('get_image/', ProjectViewSet.as_view({'get':'get_image'})),
    path('log_in/', views.obtain_auth_token, name='log_in'),
    path('users/', UserViewSet.as_view({'get':'users'})),
    path('profile/', UserViewSet.as_view({'get':'profile'})),
    path('create_account/', UserViewSet.as_view({'post':'create_account'}))
]
