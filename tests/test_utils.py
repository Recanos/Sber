import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.schemas import DepositConditions
from app.utils import calculate_monthly_deposit


def test_calculate_monthly_deposit():
    deposit = DepositConditions(
        date="31.01.2025",
        periods=3,
        amount=100000,
        rate=5
    )
    result = calculate_monthly_deposit(deposit)

    assert "31.01.2025" in result
    assert "28.02.2025" in result  # Проверка февраля
    assert "31.03.2025" in result

    assert result["31.01.2025"] == 100416.67
