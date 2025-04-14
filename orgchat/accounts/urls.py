from django.urls import path
from .views import RegisterView, UserView, UpdateOwnRoleView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('', UserView.as_view(), name='user-view'),
    path('signup/', RegisterView.as_view(), name='signup'),
    path('login/', TokenObtainPairView.as_view(), name='login'), 
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('role/update/', UpdateOwnRoleView.as_view(), name='update-own-role'),
]
