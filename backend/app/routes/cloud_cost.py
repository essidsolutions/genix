from fastapi import APIRouter, Query
from typing import Dict

router = APIRouter(prefix="/cloud-cost", tags=["Cloud Cost"])

# Mock cloud cost data
CLOUD_COST_DATA = {
    "AWS": {"total_cost": 120.75, "services": {"EC2": 45.50, "S3": 30.25, "Lambda": 45.00}},
    "Azure": {"total_cost": 98.20, "services": {"VM": 55.00, "Storage": 23.20, "Functions": 20.00}},
    "GCP": {"total_cost": 110.50, "services": {"Compute Engine": 65.00, "Cloud Storage": 25.50, "BigQuery": 20.00}},
}

@router.get("")  # ✅ Fix: Remove trailing slash to avoid redirect issues
def get_cloud_cost(provider: str = Query(None, description="Cloud Provider (AWS, Azure, GCP)")) -> Dict:
    if provider:
        return {provider: CLOUD_COST_DATA.get(provider, {"total_cost": 0, "services": {}})}
    return CLOUD_COST_DATA  # Return all if no provider specified
