from typing import Any
from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session
from api import get_db
from pydantic import UUID4

router = APIRouter(prefix="/competitions", tags=["Competitions"])

@router.get('/', status_code=status.HTTP_501_NOT_IMPLEMENTED, response_model=Any)
async def read(db: Session = Depends(get_db)):
    return Response(status_code=status.HTTP_501_NOT_IMPLEMENTED)


@router.get("/{id}", status_code=status.HTTP_501_NOT_IMPLEMENTED, response_model=Any)
async def get_by_id(id: UUID4, db: Session = Depends(get_db)):
    return Response(status_code=status.HTTP_501_NOT_IMPLEMENTED)


@router.post('/', status_code=status.HTTP_501_NOT_IMPLEMENTED, response_model=Any)
async def create(create_competition: Any, db: Session = Depends(get_db)):
    return Response(status_code=status.HTTP_501_NOT_IMPLEMENTED)


@router.put("/{id}", status_code=status.HTTP_501_NOT_IMPLEMENTED, response_model=Any)
async def update(id: UUID4, db: Session = Depends(get_db)):
    return Response(status_code=status.HTTP_501_NOT_IMPLEMENTED)


@router.delete("/{id}", status_code=status.HTTP_501_NOT_IMPLEMENTED)
async def delete(id: UUID4, db: Session = Depends(get_db)):
    return Response(status_code=status.HTTP_501_NOT_IMPLEMENTED)