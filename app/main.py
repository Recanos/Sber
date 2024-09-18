from app.schemas import DepositConditions
from app.utils import calculate_monthly_deposit
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

app = FastAPI(
    title="Калькулятор депозита!"
)


@app.post("/calculate", status_code=200)
async def calculate_deposit(deposit: DepositConditions):
    result = calculate_monthly_deposit(deposit)
    return result


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for error in exc.errors():
        errors.append({"error": str(error['input']) + " : " + error['msg']})
    return JSONResponse(status_code=400, content=errors) if len(errors) > 1\
        else JSONResponse(status_code=400, content=errors[0])
