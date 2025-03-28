from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Dict, Any, Literal
from datetime import date

class Address(BaseModel):
    line1: str
    line2: Optional[str] = None
    city: str
    state: str
    postal_code: str
    country: str = "US"

class Withholding(BaseModel):
    filing_status: str
    allowances: int = 0
    dependents: int = 0
    extra_withholdings: float = 0

class PaymentMethod(BaseModel):
    bank_name: Optional[str] = None
    account_last4: Optional[str] = None
    pay_frequency: Optional[str] = None

class EmployeeBase(BaseModel):
    first_name: str
    last_name: str
    middle_name: Optional[str] = None
    email: EmailStr
    dob: Optional[date] = None
    
class EmployeeCreate(EmployeeBase):
    residence: Optional[Address] = None
    ssn: Optional[str] = None
    payment_method_preference: str = "direct_deposit"
    active: bool = True
    w2_electronic_consent_provided: bool = True
    start_date: Optional[date] = None
    workplaces: Optional[List[str]] = None
    primary_workplace: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class EmployeeUpdate(BaseModel):
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    dob: Optional[date] = None
    residence: Optional[Address] = None
    ssn: Optional[str] = None
    payment_method_preference: Optional[str] = None
    active: Optional[bool] = None
    w2_electronic_consent_provided: Optional[bool] = None
    start_date: Optional[date] = None
    workplaces: Optional[List[str]] = None
    primary_workplace: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class EmployeeResponse(BaseModel):
    id: str
    first_name: str
    last_name: str
    middle_name: Optional[str] = None
    email: Optional[EmailStr] = None
    dob: Optional[date] = None
    ssn_last_four: Optional[str] = None
    ssn_validation_status: Optional[str] = None
    residence: Optional[Address] = None
    active: bool
    start_date: Optional[date] = None
    termination_date: Optional[date] = None
    payment_method_preference: str
    w2_electronic_consent_provided: bool
    metadata: Dict[str, Any] = {}
    
    # Additional fields for frontend compatibility
    name: Optional[str] = None
    role: Optional[str] = None
    employment_type: str = "Employee (W2)"
    
    class Config:
        orm_mode = True

    def __init__(self, **data):
        super().__init__(**data)
        # Derive name from first and last name
        if self.first_name and self.last_name:
            self.name = f"{self.first_name} {self.last_name}"
        # Get role from metadata if available
        if self.metadata and "role" in self.metadata:
            self.role = self.metadata["role"]

class OnboardingResponse(BaseModel):
    url: str
