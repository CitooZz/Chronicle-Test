from http import HTTPStatus

import pytest

from users.models import User


@pytest.mark.django_db
def test_success(api_client, users_url, user_a, change_password_payload):
    api_client.force_authenticate(user_a)
    response = api_client.post(
        f"{users_url}{user_a.id}/change-password/",
        data=change_password_payload,
    )

    assert response.status_code == HTTPStatus.NO_CONTENT
    assert (
        User.objects.get(id=user_a.id).check_password(
            change_password_payload["password"]
        )
        is True
    )


@pytest.mark.django_db
def test_not_found(api_client, users_url, user_a, change_password_payload):
    api_client.force_authenticate(user_a)
    response = api_client.post(
        f"{users_url}2000/change-password/", data=change_password_payload
    )
    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.django_db
def test_change_password_other_user(
    api_client, users_url, user_a, user_b, change_password_payload
):
    api_client.force_authenticate(user_a)
    response = api_client.post(
        f"{users_url}{user_b.id}/change-password/",
        data=change_password_payload,
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
