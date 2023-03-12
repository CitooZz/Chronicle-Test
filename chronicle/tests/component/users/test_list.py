from http import HTTPStatus

import pytest

from users.models import User


@pytest.mark.django_db
def test_success(api_client, users_url, user_a, user_b):
    api_client.force_authenticate(user_a)
    response = api_client.get(users_url)
    response_dict = response.json()

    assert response.status_code == HTTPStatus.OK
    assert response_dict["count"] == User.objects.count()
    # Check next pagination should be none
    assert response_dict["next"] is None


@pytest.mark.django_db
def test_search(api_client, users_url, user_a, user_b):
    api_client.force_authenticate(user_a)
    response = api_client.get(f"{users_url}?search=a")
    response_dict = response.json()

    assert response.status_code == HTTPStatus.OK
    assert response_dict["count"] == 1
