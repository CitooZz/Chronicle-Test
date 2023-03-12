from datetime import datetime
from http import HTTPStatus

from django.utils import timezone
import pytest


@pytest.mark.django_db
def test_success(api_client, users_url, register_payload):
    response = api_client.post(users_url, data=register_payload)

    assert response.status_code == HTTPStatus.CREATED
    assert response.data["email"] == register_payload["email"]


@pytest.mark.parametrize(
    "field",
    [
        "email",
        "password",
        "first_name",
        "date_of_birth",
        "gender",
        "confirm_password",
    ],
)
@pytest.mark.django_db
def test_empty_field(api_client, users_url, register_payload, field):
    del register_payload[field]
    response = api_client.post(users_url, data=register_payload)
    assert response.status_code == HTTPStatus.BAD_REQUEST


@pytest.mark.parametrize(
    "field, value",
    [
        ("email", "INVALID"),
        ("confirm_password", "123"),
        ("email", "test_a@test.com"),
        ("date_of_birth", datetime.strftime(timezone.now(), "%Y-%m-%d")),
    ],
)
@pytest.mark.django_db
def test_invalid_request(api_client, users_url, register_payload, field, value):
    register_payload[field] = value
    response = api_client.post(users_url, data=register_payload)
    assert response.status_code == HTTPStatus.BAD_REQUEST
