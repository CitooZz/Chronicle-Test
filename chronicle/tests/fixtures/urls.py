import pytest


@pytest.fixture
def login_url():
    return "/api/auth-token/"


@pytest.fixture
def users_url():
    return "/api/users/"
