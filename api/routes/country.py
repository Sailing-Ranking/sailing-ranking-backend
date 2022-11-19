from typing import List

from fastapi import APIRouter, status

from api.models import Country

router = APIRouter(prefix="/countries", tags=["Countries"])


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[Country])
async def read():
    """Handle returning all countries to the user."""
    return list(Country)
