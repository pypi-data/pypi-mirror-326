from typing import List, Optional
import requests
from .models import (
    DivisionResponse, FacultyResponse, PositionsResponse
)

class VPAAClient:
    def __init__(self, api_key: str, base_url: str = "https://vpaa-api-server-stnkl.ondigitalocean.app/"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "X-API-Key": api_key,
            "Accept": "application/json"
        })
    
    def get_divisions(self, departments_only: bool = False) -> DivisionResponse:
        response = self.session.get(
            f"{self.base_url}/interfolio/faculty-activity-reporting/divisions",
            params={"departments_only": departments_only}
        )
        response.raise_for_status()
        return DivisionResponse.model_validate(response.json())
    
    def get_faculty(
        self,
        unit_ids: Optional[List[int]] = None,
        tenure_statuses: Optional[List[str]] = None,
        employment_statuses: Optional[List[str]] = None
    ) -> FacultyResponse:
        params = {}
        if unit_ids:
            params["unit_ids"] = unit_ids
        if tenure_statuses:
            params["tenure_statuses"] = tenure_statuses
        if employment_statuses:
            params["employment_statuses"] = employment_statuses
            
        response = self.session.get(
            f"{self.base_url}/interfolio/faculty-activity-reporting/faculty",
            params=params
        )
        response.raise_for_status()
        return FacultyResponse.model_validate(response.json())
    
    def get_open_positions(self) -> PositionsResponse:
        response = self.session.get(
            f"{self.base_url}/interfolio/faculty-search/open-positions"
        )
        response.raise_for_status()
        return PositionsResponse.model_validate(response.json())