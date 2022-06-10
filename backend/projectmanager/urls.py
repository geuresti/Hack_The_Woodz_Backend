from django.urls import path
from .views import ProjectViewSet, UserViewSet
from rest_framework.authtoken import views
from django.contrib.auth import views as auth

# TESTING:
# projects - good
# create - good
# update - good
# delete - good
# view - good
# thumbnail - good (needed?)
# profile - good

urlpatterns = [
    path('projects/', ProjectViewSet.as_view({'get':'projects'})),
    path('create/', ProjectViewSet.as_view({'post':'create'})),
    path('update/', ProjectViewSet.as_view({'post':'update'})),
    path('delete_project/', ProjectViewSet.as_view({'delete':'delete_project'})),
    path('view_project/', ProjectViewSet.as_view({'get':'view_project'})),
    path('get_thumbnail/', ProjectViewSet.as_view({'get':'get_thumbnail'})),
    path('log_in/', views.obtain_auth_token, name='log_in'),
    path('log_out/', UserViewSet.as_view({'delete':'log_out'})),
    path('users/', UserViewSet.as_view({'get':'users'})),
    path('profile/', UserViewSet.as_view({'get':'profile'})),
    path('create_account/', UserViewSet.as_view({'post':'create_account'}))
]
