from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator
import math
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


@app.post("/add")
async def add_numbers(request: MathRequest) -> MathResponse:
    try:
        result = add(request.a, request.b)
        if not math.isfinite(result):
            raise HTTPException(status_code=400, detail="Result is not a finite number")
        return MathResponse(result=result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/subtract")
async def subtract_numbers(request: MathRequest) -> MathResponse:
    try:
        result = subtract(request.a, request.b)
        if not math.isfinite(result):
            raise HTTPException(status_code=400, detail="Result is not a finite number")
        return MathResponse(result=result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/multiply")
async def multiply_numbers(request: MathRequest) -> MathResponse:
    try:
        result = multiply(request.a, request.b)
        if not math.isfinite(result):
            raise HTTPException(status_code=400, detail="Result is not a finite number")
        return MathResponse(result=result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/divide")
async def divide_numbers(request: MathRequest) -> MathResponse:
    try:
        result = divide(request.a, request.b)
        if not math.isfinite(result):
            raise HTTPException(status_code=400, detail="Result is not a finite number")
        return MathResponse(result=result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
