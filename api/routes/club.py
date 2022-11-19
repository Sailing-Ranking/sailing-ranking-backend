from typing import List

from fastapi import APIRouter, status

from api.models import Club

router = APIRouter(prefix="/clubs", tags=["Clubs"])


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[Club])
async def read():
    """Handle returning all countries to the user."""
    return list(Club)
