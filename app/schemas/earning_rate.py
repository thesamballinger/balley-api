from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, Literal

class EarningRateBase(BaseModel):
    amount: float
    period: Literal["hourly", "daily", "weekly", "biweekly", "semimonthly", "monthly", "annually"]
    workweek_hours: float = 40.0
    name: Optional[str] = None

class EarningRateCreate(EarningRateBase):
    employee: str
    metadata: Optional[Dict[str, Any]] = None

class EarningRateUpdate(BaseModel):
    active: bool

class EarningRateResponse(BaseModel):
    id: str
    employee: str
    amount: float
    period: str
    active: bool
    name: Optional[str] = None
    workweek_hours: float
    metadata: Dict[str, Any] = {}
    
    class Config:
        orm_mode = True
