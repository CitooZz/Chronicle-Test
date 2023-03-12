from django.utils import timezone
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


from users.models import User


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.all_objects.all())],
    )
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "date_of_birth",
            "gender",
            "address",
            "password",
            "confirm_password",
        ]

    def validate_date_of_birth(self, value):
        if value >= timezone.now().date():
            raise serializers.ValidationError(
                {"date_of_birth": "Can't be future date."}
            )

        return value

    def validate(self, value):
        if value.get("password") != value.get("confirm_password"):
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )

        return value

    def create(self, validated_data):
        "Customize user creation process."
        del validated_data["confirm_password"]
        password = validated_data.pop("password")
        user = User.objects.create(**validated_data, is_active=True)
        user.set_password(password)
        user.save()
        return user


class UserChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    password = serializers.CharField(required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = self.context.get("user")
        self.request = self.context.get("request")

    def validate(self, value):
        if value.get("password") != value.get("confirm_password"):
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )

        if self.user != self.request.user:
            raise serializers.ValidationError("You can't change other user password.")

        if not self.user.check_password(value.get("old_password")):
            raise serializers.ValidationError(
                {"old_password": "Current Password is invalid."}
            )

        return value
