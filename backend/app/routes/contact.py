from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import ContactLead
from ..schemas import (
    ContactLeadCreate,
    ContactLeadResponse,
    ContactLeadStatusUpdate,
)
from ..services.email import send_contact_notification


router = APIRouter(
    prefix="/api/contact",
    tags=["Contact"],
)


VALID_STATUSES = {
    "NEW",
    "CONTACTED",
    "IN PROGRESS",
    "COMPLETED",
}


@router.post(
    "",
    response_model=ContactLeadResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_contact_lead(
    payload: ContactLeadCreate,
    db: Session = Depends(get_db),
):
    lead = ContactLead(
        name=payload.name.strip(),
        email=str(payload.email),
        project_type=payload.project_type.strip(),
        message=payload.message.strip(),
        status="NEW",
    )

    db.add(lead)
    db.commit()
    db.refresh(lead)

    # Save the lead first. Email failure should not destroy the lead.
    try:
        send_contact_notification(
            name=lead.name,
            email=lead.email,
            project_type=lead.project_type,
            message=lead.message,
        )
    except Exception as exc:
        print(
            f"WARNING: Lead #{lead.id} saved, "
            f"but email notification failed: {exc}"
        )

    return lead


@router.get(
    "",
    response_model=list[ContactLeadResponse],
)
def get_contact_leads(
    db: Session = Depends(get_db),
):
    statement = (
        select(ContactLead)
        .order_by(ContactLead.created_at.desc())
    )

    leads = db.scalars(statement).all()

    return leads


@router.get(
    "/{lead_id}",
    response_model=ContactLeadResponse,
)
def get_contact_lead(
    lead_id: int,
    db: Session = Depends(get_db),
):
    lead = db.get(ContactLead, lead_id)

    if not lead:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lead not found.",
        )

    return lead


@router.patch(
    "/{lead_id}/status",
    response_model=ContactLeadResponse,
)
def update_contact_lead_status(
    lead_id: int,
    payload: ContactLeadStatusUpdate,
    db: Session = Depends(get_db),
):
    new_status = payload.status.strip().upper()

    if new_status not in VALID_STATUSES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Invalid status. Use one of: "
                "NEW, CONTACTED, IN PROGRESS, COMPLETED."
            ),
        )

    lead = db.get(ContactLead, lead_id)

    if not lead:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lead not found.",
        )

    lead.status = new_status

    db.commit()
    db.refresh(lead)

    return lead


@router.delete(
    "/{lead_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_contact_lead(
    lead_id: int,
    db: Session = Depends(get_db),
):
    lead = db.get(ContactLead, lead_id)

    if not lead:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lead not found.",
        )

    db.delete(lead)
    db.commit()

    return None