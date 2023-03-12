from http import HTTPStatus

import pytest


@pytest.mark.django_db
def test_success(api_client, users_url, user_a, update_payload):
    api_client.force_authenticate(user_a)
    response = api_client.patch(f"{users_url}{user_a.id}/", data=update_payload)
    response_dict = response.json()

    assert response.status_code == HTTPStatus.OK
    for key, value in update_payload.items():
        assert response_dict[key] == value


@pytest.mark.django_db
def test_not_found(api_client, users_url, user_a, update_payload):
    api_client.force_authenticate(user_a)
    response = api_client.patch(f"{users_url}2000/", data=update_payload)
    assert response.status_code == HTTPStatus.NOT_FOUND
