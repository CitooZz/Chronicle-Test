import pytest

from users.models import GenderChoice


@pytest.fixture
def login_payload():
    return {"email": "test_a@test.com", "password": "test1234"}


@pytest.fixture
def register_payload():
    return {
        "email": "test@test.com",
        "first_name": "test",
        "last_name": "test",
        "gender": GenderChoice.MALE,
        "date_of_birth": "2001-03-1",
        "address": "Jakarta",
        "password": "test1234!@",
        "confirm_password": "test1234!@",
    }


@pytest.fixture
def update_payload():
    return {"first_name": "updated", "gender": GenderChoice.FEMALE}


@pytest.fixture
def change_password_payload():
    return {
        "old_password": "test1234",
        "password": "test1234!@",
        "confirm_password": "test1234!@",
    }
