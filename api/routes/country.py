from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from api import get_db
from api.models import Country

router = APIRouter(prefix="/countries", tags=["Countries"])


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[Country])
async def read(db: Session = Depends(get_db)):
    """Handle returning all countries to the user."""
    return list(Country)
