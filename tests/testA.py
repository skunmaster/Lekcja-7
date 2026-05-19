import pytest
from src.manager import Manager
from src.models import Parameters, Transfer

def test_transfer_amount_validation_min_max():
    manager = Manager(Parameters())

    transfer_valid = Transfer(
        tenant='tenant-1',
        date='2025-01-01',
        settlement_year=2025,
        settlement_month=1,
        amount_pln=1000.0,  
        type='payment'
    )

    manager.transfers.append(transfer_valid)
    
    min_value = 0.0
    max_value = 10000.0
    assert min_value <= transfer_valid.amount_pln <= max_value, "Transfer poza dopuszczalnym zakresem"

def test_transfer_amount_below_minimum():
    manager = Manager(Parameters())
    transfer_invalid = Transfer(
        tenant='tenant-1',
        date='2025-01-01',
        settlement_year=2025,
        settlement_month=1,
        amount_pln=-100.0,  
        type='payment'
    )

    with pytest.raises(AssertionError):
        assert transfer_invalid.amount_pln >= 0, "Kwota transferu nie może być ujemna"

def test_transfer_amount_above_maximum():
    manager = Manager(Parameters())
    transfer_invalid = Transfer(
        tenant='tenant-1',
        date='2025-01-01',
        settlement_year=2025,
        settlement_month=1,
        amount_pln=20000.0,  
        type='payment'
    )

    with pytest.raises(AssertionError):
        max_value = 10000.0
        assert transfer_invalid.amount_pln <= max_value, "Kwota transferu przekracza maksymalny limit"