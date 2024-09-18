import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_example():
    assert 1 + 1 == 2


def test_calculate_deposit_valid_data():
    valid_data = {
        "date": "31.01.2025",
        "periods": 3,
        "amount": 100000,
        "rate": 5
    }
    response = client.post("/calculate", json=valid_data)

    assert response.status_code == 200
    result = response.json()

    assert "31.01.2025" in result
    assert "28.02.2025" in result  # проверка обработки февраля
    assert "31.03.2025" in result


def test_calculate_deposit_invalid_date_format():
    invalid_data = {
        "date": "31-01-2025",  # неправильный формат
        "periods": 3,
        "amount": 100000,
        "rate": 5
    }
    response = client.post("/calculate", json=invalid_data)

    assert response.status_code == 400
    result = response.json()
    assert "31-01-2025" in result["error"]
    assert "31-01-2025 : Value error, date must be in dd.mm.YYYY format" in result["error"]


def test_calculate_deposit_invalid_periods():
    invalid_data = {
        "date": "31.01.2025",
        "periods": 100,  # слишком большое количество
        "amount": 100000,
        "rate": 5
    }
    response = client.post("/calculate", json=invalid_data)

    assert response.status_code == 400
    result = response.json()
    assert "100 : Input should be less than or equal to 60" in result["error"]


def test_calculate_deposit_invalid_amount():
    invalid_data = {
        "date": "31.01.2025",
        "periods": 3,
        "amount": 5000,  # слишком маленькая сумма
        "rate": 5
    }
    response = client.post("/calculate", json=invalid_data)

    assert response.status_code == 400
    result = response.json()
    assert "5000 : Input should be greater than or equal to 10000" in result["error"]


def test_calculate_deposit_invalid_rate():
    invalid_data = {
        "date": "31.01.2025",
        "periods": 3,
        "amount": 100000,
        "rate": 10  # слишком большая ставка
    }
    response = client.post("/calculate", json=invalid_data)

    assert response.status_code == 400
    result = response.json()
    assert "10 : Input should be less than or equal to 8" in result["error"]
