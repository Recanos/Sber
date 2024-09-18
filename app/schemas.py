from datetime import datetime

from pydantic import BaseModel, Field, field_validator


class DepositConditions(BaseModel):
    date: str = Field(description="Дата депозита в формате dd.mm.YYYY", example="31.01.2025")
    periods: int = Field(ge=1, le=60, description="Количество периодов должно быть от 1 до 60", example=3)
    amount: int = Field(ge=10000, le=3000000, description="Сумма должна быть от 10,000 до 3,000,000", example=10000)
    rate: float = Field(ge=1.0, le=8.0, description="Ставка должна быть от 1 до 8", example=6)

    @field_validator('date')
    def validate_date_format(cls, value):
        try:
            parsed_date = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("date must be in dd.mm.YYYY format")
        if parsed_date < datetime.now().date():
            raise ValueError("date must be >= current")  # могу убрать, если не надо
        return value
