from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenObtainPairView,
)

from users.views import UserViewSet

router = routers.DefaultRouter()
router.register(r"users", UserViewSet, basename="users")

urlpatterns = [
    path("", include(router.urls)),
    path(
        "auth-token/",
        TokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path("refresh-token/", TokenRefreshView.as_view(), name="token_refresh"),
]
