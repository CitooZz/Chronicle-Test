from http import HTTPStatus

from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


from users.serializers import (
    UserSerializer,
    UserChangePasswordSerializer,
)

from users.models import User


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    search_fields = ["email", "first_name", "last_name"]
    ordering_fields = "__all__"
    no_authentication_actions = ["create"]

    def get_permissions(self):
        """Customize get permissions."""
        if self.action in self.no_authentication_actions:
            return (AllowAny(),)

        return super().get_permissions()

    @method_decorator(cache_page(settings.CACHE_TTL))
    @method_decorator(
        vary_on_headers(
            "Authorization",
        )
    )
    def list(self, *args, **kwargs):
        """Customize get user list."""
        return super().list(*args, **kwargs)

    @action(
        detail=True,
        methods=["POST"],
        serializer_class=UserChangePasswordSerializer,
        url_path="change-password",
    )
    def change_password(self, request, pk):
        """User change password."""
        user = self.get_object()
        serializer = self.serializer_class(
            data=request.data, context={"user": user, "request": request}
        )
        serializer.is_valid(raise_exception=True)
        user.set_password(serializer.validated_data.get("password"))
        user.save()
        return Response(status=HTTPStatus.NO_CONTENT)
