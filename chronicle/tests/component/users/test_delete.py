from http import HTTPStatus

import pytest

from users.models import User


@pytest.mark.django_db
def test_success(api_client, users_url, user_a, user_b):
    api_client.force_authenticate(user_a)
    response = api_client.delete(f"{users_url}{user_b.id}/")

    assert response.status_code == HTTPStatus.NO_CONTENT
    assert User.objects.count() == 1


@pytest.mark.django_db
def test_not_found(api_client, users_url, user_a):
    api_client.force_authenticate(user_a)
    response = api_client.delete(f"{users_url}2000/")
    assert response.status_code == HTTPStatus.NOT_FOUND
