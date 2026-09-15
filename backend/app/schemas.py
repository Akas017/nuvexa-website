from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class ContactLeadCreate(BaseModel):
    name: str
    email: EmailStr
    project_type: str
    message: str


class ContactLeadStatusUpdate(BaseModel):
    status: str


class ContactLeadResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    project_type: str
    message: str
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)