from django.urls import path
from .views import *
from . import views
from rest_framework.authtoken.views import obtain_auth_token




urlpatterns = [
    # URL PATTERNS TO CREATE A USER AND AUTHENTICATE
    path('register/', views.register.as_view(), name="register"),
    path('login/', obtain_auth_token, name="login"),

    # URL TO PERFORM CRUD ON USERS
    path('userDetails/<int:pk>/', views.userDetails.as_view(), name="userDetails"),

    # URLS PATTERNS THAT PERFORM CRUD ON ROLES MODEL
    # path('userRoles/<int:pk>/', views.userRoles.as_view(), name='userRoles'),
    path('roleview/', views.RoleViewSet.as_view({'get': 'list'}), name="roleview"),
    path('roleview/', views.RoleViewSet.as_view({'post':'create'}), name='roleview-create'),
    path('roleview/<int:pk>/', views.RoleViewSet.as_view({'put':'update'}), name='roleview-update'),
    path('roleview/<int:pk>/', views.RoleViewSet.as_view({'delete':'destroy'}), name='roleview-delete'),

    # URLS PATTERNS THAT PERFORM CRUD ON RIGHTS MODEL
    path('rightsview/', views.RightsViewSet.as_view({'get':'list'}), name='rightsview'),
    path('rightsview/', views.RightsViewSet.as_view({'post': 'create'}), name='rightsview-create'),
    path('rightsview/<int:pk>/', views.RightsViewSet.as_view({'put':'update'}), name='rightsview-update'),
    path('rightsview/<int:pk>/', views.RightsViewSet.as_view({'delete':'destroy'}), name='rightsview-delete')
]