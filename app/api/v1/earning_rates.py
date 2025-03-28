from fastapi import APIRouter, HTTPException, status, Query
from typing import List, Optional
from app.schemas.earning_rate import EarningRateCreate, EarningRateUpdate, EarningRateResponse
from app.services.check_api import check_api_service

router = APIRouter(prefix="/earning_rates", tags=["earning_rates"])

@router.get("/", response_model=List[EarningRateResponse])
async def get_earning_rates(employee: Optional[str] = Query(None)):
    """
    Get all earning rates, optionally filtered by employee.
    """
    try:
        if employee:
            rates = await check_api_service.get_employee_earning_rates(employee)
        else:
            rates = await check_api_service.get_earning_rates()
        return rates
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch earning rates: {str(e)}"
        )

@router.post("/", response_model=EarningRateResponse, status_code=status.HTTP_201_CREATED)
async def create_earning_rate(rate: EarningRateCreate):
    """
    Create a new earning rate.
    """
    try:
        created_rate = await check_api_service.create_earning_rate(rate.dict(exclude_unset=True))
        return created_rate
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create earning rate: {str(e)}"
        )

@router.patch("/{rate_id}", response_model=EarningRateResponse)
async def update_earning_rate(rate_id: str, rate: EarningRateUpdate):
    """
    Update an earning rate (only active status can be changed).
    """
    try:
        updated_rate = await check_api_service.update_earning_rate(rate_id, rate.active)
        return updated_rate
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to update earning rate: {str(e)}"
        )
