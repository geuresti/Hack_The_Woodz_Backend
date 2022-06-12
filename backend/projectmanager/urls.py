from django.urls import path
from .views import CustomAuthToken, ProjectViewSet, UserViewSet

urlpatterns = [
    path('delete_all_projects/', ProjectViewSet.as_view({'delete':'delete_all_projects'})),
    path('projects/', ProjectViewSet.as_view({'get':'projects'})),
    path('create/', ProjectViewSet.as_view({'post':'create'})),
    path('update/', ProjectViewSet.as_view({'post':'update'})),
    path('delete_project/', ProjectViewSet.as_view({'delete':'delete_project'})),
    path('view_project/', ProjectViewSet.as_view({'get':'view_project'})),
    path('get_thumbnail/', ProjectViewSet.as_view({'get':'get_thumbnail'})),
    path('log_in/', CustomAuthToken.as_view()),
    path('log_out/', UserViewSet.as_view({'delete':'log_out'})),
    path('users/', UserViewSet.as_view({'get':'users'})),
    path('profile/', UserViewSet.as_view({'get':'profile'})),
    path('create_account/', UserViewSet.as_view({'post':'create_account'}))
]
