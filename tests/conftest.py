import copy

import pytest
from fastapi.testclient import TestClient

from src.app import activities as activities_store, app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    original_activities = copy.deepcopy(activities_store)
    yield
    activities_store.clear()
    activities_store.update(original_activities)
