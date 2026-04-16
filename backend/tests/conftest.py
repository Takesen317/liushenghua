"""
Pytest fixtures for tests
"""
import pytest


@pytest.fixture(autouse=True)
def clear_rate_limit():
    """Clear rate limit storage between tests"""
    from app.api.v1.auth import _rate_limit_storage
    _rate_limit_storage.clear()
    yield
    _rate_limit_storage.clear()
