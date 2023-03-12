import pytest


from rest_framework.test import APIClient

from users.models import User, GenderChoice


@pytest.fixture(autouse=True)
def user_a():
    """Initialize test user."""
    return User.objects.create_user(
        "test_a@test.com",
        "test1234",
        **{
            "first_name": "test",
            "last_name": "a",
            "gender": GenderChoice.MALE,
            "date_of_birth": "2001-03-11",
        },
    )


@pytest.fixture(autouse=True)
def user_b():
    """Initialize test user."""
    return User.objects.create_user(
        "test_b@test.com",
        "test1234",
        **{
            "first_name": "test",
            "last_name": "b",
            "gender": GenderChoice.FEMALE,
            "date_of_birth": "2001-03-11",
        },
    )


@pytest.fixture
def api_client():
    return APIClient()
