import httpx
from typing import Dict, Any, Optional, List
from app.config import get_settings

settings = get_settings()

class CheckAPIService:
    def __init__(self):
        self.base_url = settings.check_api_url
        self.headers = {
            "Authorization": f"Bearer {settings.check_api_key}",
            "Content-Type": "application/json"
        }
        self.company_id = settings.check_company_id
    
    async def _make_request(self, method: str, endpoint: str, params: Optional[Dict[str, Any]] = None, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a request to the Check API"""
        url = f"{self.base_url}{endpoint}"
        
        async with httpx.AsyncClient() as client:
            response = await client.request(
                method=method,
                url=url,
                headers=self.headers,
                params=params,
                json=data,
                timeout=30.0
            )
            
            response.raise_for_status()
            return response.json()
    
    # Employee methods
    async def get_employees(self) -> List[Dict[str, Any]]:
        """Get all employees for the company"""
        params = {"company": self.company_id}
        response = await self._make_request("GET", "/employees", params=params)
        return response.get("results", [])
    
    async def get_employee(self, employee_id: str) -> Dict[str, Any]:
        """Get a specific employee by ID"""
        return await self._make_request("GET", f"/employees/{employee_id}")
    
    async def create_employee(self, employee_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new employee"""
        # Ensure company ID is included
        employee_data["company"] = self.company_id
        return await self._make_request("POST", "/employees", data=employee_data)
    
    async def update_employee(self, employee_id: str, employee_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing employee"""
        return await self._make_request("PATCH", f"/employees/{employee_id}", data=employee_data)
    
    async def onboard_employee(self, employee_id: str) -> Dict[str, Any]:
        """Generate onboarding URL for an employee"""
        return await self._make_request("POST", f"/employees/{employee_id}/onboard")
    
    # Earning rate methods
    async def get_earning_rates(self) -> List[Dict[str, Any]]:
        """Get all earning rates"""
        response = await self._make_request("GET", "/earning_rates")
        return response.get("results", [])
    
    async def get_employee_earning_rates(self, employee_id: str) -> List[Dict[str, Any]]:
        """Get earning rates for a specific employee"""
        params = {"employee": employee_id}
        response = await self._make_request("GET", "/earning_rates", params=params)
        return response.get("results", [])
    
    async def create_earning_rate(self, rate_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new earning rate"""
        return await self._make_request("POST", "/earning_rates", data=rate_data)
    
    async def update_earning_rate(self, rate_id: str, active: bool) -> Dict[str, Any]:
        """Update an earning rate (only active status can be changed)"""
        return await self._make_request("PATCH", f"/earning_rates/{rate_id}", data={"active": active})

# Create a singleton instance
check_api_service = CheckAPIService()
