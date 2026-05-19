import pytest

# Dane przykładowe najemców
tenant_1 = {
    "id": "tenant-1",
    "name": "Jan Kowalski",
    "rent_amount": 1000.0,
    "lease_start": "2026-01-01",
    "lease_end": "2026-12-31"
}

tenant_2 = {
    "id": "tenant-2",
    "name": "Anna Nowak",
    "rent_amount": 1500.0,
    "lease_start": "2026-03-01",
    "lease_end": "2026-08-31"
}

# Przelewy testowe
payment_ok = {
    "tenant_id": "tenant-1",
    "amount": 1000.0,
    "date": "2026-02-01"
}

payment_wrong_tenant = {
    "tenant_id": "tenant-999",  # nieistniejący najemca
    "amount": 1000.0,
    "date": "2026-02-01"
}

payment_wrong_amount = {
    "tenant_id": "tenant-2",
    "amount": 2000.0,  # kwota niezgodna z umową
    "date": "2026-04-01"
}

payment_out_of_period = {
    "tenant_id": "tenant-2",
    "amount": 1500.0,
    "date": "2027-01-01"  # poza okresem najmu
}

# Klasa systemu do sprawdzania przelewów
class PaymentChecker:
    def __init__(self, tenants: dict):
        self.tenants = tenants  # dict: tenant_id -> tenant_data

    def check_payment(self, payment: dict) -> list[str]:
        errors = []

        tenant_id = payment.get("tenant_id")
        tenant = self.tenants.get(tenant_id)

        if not tenant:
            errors.append("Payment not assigned to existing tenant.")
            return errors

        if payment["amount"] != tenant["rent_amount"]:
            errors.append("Payment amount does not match lease agreement.")

        payment_date = payment["date"]
        if payment_date < tenant["lease_start"] or payment_date > tenant["lease_end"]:
            errors.append("Payment date is outside of lease period.")

        return errors

# Testy funkcjonalne
def test_payment_ok():
    tenants = {"tenant-1": tenant_1, "tenant-2": tenant_2}
    checker = PaymentChecker(tenants)
    errors = checker.check_payment(payment_ok)
    assert errors == []

def test_payment_wrong_tenant():
    tenants = {"tenant-1": tenant_1, "tenant-2": tenant_2}
    checker = PaymentChecker(tenants)
    errors = checker.check_payment(payment_wrong_tenant)
    assert "Payment not assigned to existing tenant." in errors

def test_payment_wrong_amount():
    tenants = {"tenant-1": tenant_1, "tenant-2": tenant_2}
    checker = PaymentChecker(tenants)
    errors = checker.check_payment(payment_wrong_amount)
    assert "Payment amount does not match lease agreement." in errors

def test_payment_out_of_period():
    tenants = {"tenant-1": tenant_1, "tenant-2": tenant_2}
    checker = PaymentChecker(tenants)
    errors = checker.check_payment(payment_out_of_period)
    assert "Payment date is outside of lease period." in errors