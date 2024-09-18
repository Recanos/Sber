import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from app.schemas import DepositConditions
from pydantic import ValidationError


def test_valid_deposit_conditions():
    deposit = DepositConditions(
        date="31.01.2025",
        periods=3,
        amount=100000,
        rate=5
    )
    assert deposit.date == "31.01.2025"
    assert deposit.periods == 3
    assert deposit.amount == 100000
    assert deposit.rate == 5


def test_invalid_date_format():
    with pytest.raises(ValidationError) as excinfo:
        DepositConditions(
            date="31-01-2025",  # неверный формат
            periods=3,
            amount=100000,
            rate=5
        )
    assert "date must be in dd.mm.YYYY format" in str(excinfo.value)


def test_invalid_periods():
    with pytest.raises(ValidationError) as excinfo:
        DepositConditions(
            date="31.01.2025",
            periods=100,  # слишком большое количество
            amount=100000,
            rate=5
        )
    assert "Input should be less than or equal to 60 [type=less_than_equal, input_value=100, input_type=int]" in str(
        excinfo.value)


def test_invalid_amount():
    with pytest.raises(ValidationError) as excinfo:
        DepositConditions(
            date="31.01.2025",
            periods=3,
            amount=5000,  # слишком маленькая сумма
            rate=5
        )
    assert ("Input should be greater than or equal to 10000 [type=greater_than_equal, input_value=5000, input_type=int]"
            in str(excinfo.value))


def test_invalid_rate():
    with pytest.raises(ValidationError) as excinfo:
        DepositConditions(
            date="31.01.2025",
            periods=3,
            amount=100000,
            rate=10  # слишком большая ставка
        )
    assert ("Input should be less than or equal to 8 [type=less_than_equal, input_value=10, input_type=int]"
            in str(excinfo.value))
