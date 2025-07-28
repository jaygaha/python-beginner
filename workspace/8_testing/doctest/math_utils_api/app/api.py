from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator
import math
from typing import Callable
from app.calculator import add, divide, multiply, subtract

app = FastAPI()


class MathRequest(BaseModel):
    a: float
    b: float

    @field_validator("a", "b")
    @classmethod
    def validate_finite_numbers(cls, v):
        if not math.isfinite(v):
            raise ValueError("Only finite numbers are allowed")
        return v


class MathResponse(BaseModel):
    result: float


def _calculate(
    request: MathRequest, operation: Callable[[float, float], float]
) -> MathResponse:
    """
    Helper function to perform a calculation, handle errors, and return a response.
    """
    try:
        result = operation(request.a, request.b)
        if not math.isfinite(result):
            raise HTTPException(
                status_code=400, detail="Result is not a finite number"
            )
        return MathResponse(result=result)
    except ValueError as e:
        # This will catch "Cannot divide by zero"
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Catch any other unexpected errors
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/add", response_model=MathResponse)
async def add_numbers(request: MathRequest):
    return _calculate(request, add)


@app.post("/subtract", response_model=MathResponse)
async def subtract_numbers(request: MathRequest):
    return _calculate(request, subtract)


@app.post("/multiply", response_model=MathResponse)
async def multiply_numbers(request: MathRequest):
    return _calculate(request, multiply)


@app.post("/divide", response_model=MathResponse)
async def divide_numbers(request: MathRequest):
    return _calculate(request, divide)
