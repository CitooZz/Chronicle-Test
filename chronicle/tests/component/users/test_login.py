from http import HTTPStatus

import pytest


@pytest.mark.django_db
def test_success(api_client, login_url, login_payload):
    response = api_client.post(login_url, data=login_payload)
    response_dict = response.json()

    assert response.status_code == HTTPStatus.OK
    assert "access" in response_dict


@pytest.mark.parametrize(
    "field, value",
    [
        ("password", "invalid"),
        ("email", "invalid-email"),
    ],
)
@pytest.mark.django_db
def test_invalid_credential(api_client, login_url, login_payload, field, value):
    login_payload[field] = value
    response = api_client.post(login_url, data=login_payload)
    assert response.status_code == HTTPStatus.UNAUTHORIZED


@pytest.mark.parametrize(
    "field",
    ["email", "password"],
)
@pytest.mark.django_db
def test_empty_field(api_client, login_url, login_payload, field):
    del login_payload[field]
    response = api_client.post(login_url, data=login_payload)
    assert response.status_code == HTTPStatus.BAD_REQUEST
