from datetime import date, timedelta, datetime
from typing import List

from fastapi import Depends, HTTPException, Path, status, APIRouter, Query
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User
from src.repository import contacts as repository_contacts
from src.schemas import ContactModel, ContactResponse
from src.services.auth import auth_service
from fastapi_limiter.depends import RateLimiter

router = APIRouter(prefix="/contacts", tags=['contacts'])


@router.get("/", response_model=List[ContactResponse], dependencies=[Depends(RateLimiter(times=10, seconds=10))])
async def get_contacts(limit: int = Query(10, le=500), offset: int = 0, db: Session = Depends(get_db),
                       current_user: User = Depends(auth_service.get_current_user)):
    contacts = await repository_contacts.get_contacts(limit, offset, current_user, db)
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse)
async def get_contact(contact_id: int = Path(ge=1), db: Session = Depends(get_db),
                      current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.get_contact_by_id(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


@router.get("/by_email/{email}", response_model=ContactResponse)
async def get_contact_by_email(email: str, db: Session = Depends(get_db),
                               current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.get_contact_by_email(email, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


@router.get("/by_phone/{phone}", response_model=ContactResponse)
async def get_contact_by_phone(phone: str, db: Session = Depends(get_db),
                               current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.get_contact_by_phone(phone, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


@router.get("/by_first_name/{first_name}", response_model=ContactResponse)
async def get_contact_by_first_name(first_name: str, db: Session = Depends(get_db),
                                    current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.get_contact_by_first_name(first_name, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


@router.get("/by_second_name/{second_name}", response_model=ContactResponse)
async def get_contact_by_second_name(second_name: str, db: Session = Depends(get_db),
                                     current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.get_contact_by_second_name(second_name, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


@router.get("/by_birth_date/{birth_date}", response_model=ContactResponse)
async def get_contact_by_birth_date(birth_date: date, db: Session = Depends(get_db),
                                    current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.get_contact_by_birth_date(birth_date, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(body: ContactModel, db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.create(body, current_user, db)
    return contact


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(body: ContactModel, contact_id: int = Path(ge=1), db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.update(contact_id, body, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_contact(contact_id: int = Path(ge=1), db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.remove(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


@router.get("/birthday_list/", response_model=list[ContactResponse])
async def get_birthday_list(db: Session = Depends(get_db),
                            current_user: User = Depends(auth_service.get_current_user)):
    start_date = datetime.now().date()
    delta = 7
    end_date = start_date + timedelta(days=delta)
    contacts = await repository_contacts.get_contacts_birthday(start_date, end_date, current_user, db)
    return contacts
