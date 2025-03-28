from fastapi import APIRouter, HTTPException, status, Depends, Query
from typing import List, Optional
from app.schemas.employee import EmployeeCreate, EmployeeUpdate, EmployeeResponse, OnboardingResponse
from app.services.check_api import check_api_service

router = APIRouter(prefix="/employees", tags=["employees"])

@router.get("/", response_model=List[EmployeeResponse])
async def get_employees():
    """
    Get all employees for the company.
    """
    try:
        employees = await check_api_service.get_employees()
        return employees
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch employees: {str(e)}"
        )

@router.get("/{employee_id}", response_model=EmployeeResponse)
async def get_employee(employee_id: str):
    """
    Get a specific employee by ID.
    """
    try:
        employee = await check_api_service.get_employee(employee_id)
        return employee
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee not found: {str(e)}"
        )

@router.post("/", response_model=EmployeeResponse, status_code=status.HTTP_201_CREATED)
async def create_employee(employee: EmployeeCreate):
    """
    Create a new employee.
    """
    try:
        created_employee = await check_api_service.create_employee(employee.dict(exclude_unset=True))
        return created_employee
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create employee: {str(e)}"
        )

@router.patch("/{employee_id}", response_model=EmployeeResponse)
async def update_employee(employee_id: str, employee: EmployeeUpdate):
    """
    Update an existing employee.
    """
    try:
        updated_employee = await check_api_service.update_employee(
            employee_id, 
            employee.dict(exclude_unset=True, exclude_none=True)
        )
        return updated_employee
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to update employee: {str(e)}"
        )

@router.post("/{employee_id}/onboard", response_model=OnboardingResponse)
async def onboard_employee(employee_id: str):
    """
    Generate onboarding URL for an employee.
    """
    try:
        onboarding_data = await check_api_service.onboard_employee(employee_id)
        return onboarding_data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to generate onboarding URL: {str(e)}"
        )
