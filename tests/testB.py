import pytest
from src.manager import Manager

@pytest.fixture
def manager():
    return Manager()

@pytest.fixture
def mock_blacklist(monkeypatch):
    blacklist = [
        {"first_name": "Jan", "last_name": "Nowak", "reason": "nieopłacone rachunki"},
        {"first_name": "Anna", "last_name": "Kowalska", "reason": "naruszenie regulaminu"}
    ]

    def mock_get_blacklist(self):
        return blacklist
    monkeypatch.setattr(Manager, "get_blacklist", mock_get_blacklist)

def test_tenant_on_blacklist(manager, mock_blacklist):
    tenant = {"first_name": "Jan", "last_name": "Nowak"}
    assert manager.is_tenant_blacklisted(tenant) is True

def test_tenant_not_on_blacklist(manager, mock_blacklist):
    tenant = {"first_name": "Adam", "last_name": "Kowalski"}
    assert manager.is_tenant_blacklisted(tenant) is False