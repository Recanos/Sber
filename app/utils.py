from datetime import datetime
from typing import Dict

from app.schemas import DepositConditions
from dateutil.relativedelta import relativedelta


def calculate_monthly_deposit(deposit: DepositConditions) -> Dict[str, float]:
    result = {}
    current_date = datetime.strptime(deposit.date, "%d.%m.%Y")
    current_amount = deposit.amount

    def get_last_day_of_month(date: datetime) -> datetime:
        next_month = date + relativedelta(months=1)
        return next_month.replace(day=1) - relativedelta(days=1)

    current_amount *= (1 + deposit.rate / 12 / 100)
    result[current_date.strftime("%d.%m.%Y")] = round(current_amount, 2)

    original_day = current_date.day

    for month in range(1, deposit.periods):
        next_date = current_date + relativedelta(months=1)
        try:
            current_date = next_date.replace(day=original_day)
        except ValueError:
            current_date = get_last_day_of_month(next_date)

        current_amount *= (1 + deposit.rate / 12 / 100)
        result[current_date.strftime("%d.%m.%Y")] = round(current_amount, 2)

    return result
