from http import HTTPStatus

import pytest


@pytest.mark.django_db
def test_success(api_client, users_url, user_a):
    api_client.force_authenticate(user_a)
    response = api_client.get(f"{users_url}{user_a.id}/")
    response_dict = response.json()

    assert response.status_code == HTTPStatus.OK
    assert response_dict["email"] == user_a.email


@pytest.mark.django_db
def test_not_found(api_client, users_url, user_a):
    api_client.force_authenticate(user_a)
    response = api_client.get(f"{users_url}2000/")
    assert response.status_code == HTTPStatus.NOT_FOUND
