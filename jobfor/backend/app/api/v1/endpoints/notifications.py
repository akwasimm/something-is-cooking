from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.async_database import get_async_db
from app.api.dependencies.auth import get_current_user
from app.models.models import User
from app.schemas.notification import NotificationResponse, JobAlertCreate
from app.services.notification_service import NotificationService


router = APIRouter(prefix="/notifications", tags=["Notifications & Alerts"])


@router.get("/", response_model=List[NotificationResponse])
async def list_notifications(
    unread_only: bool = False,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    """
    Returns array mapping user-targeted actions. 
    """
    return await NotificationService.get_notifications(db, current_user.id, unread_only)


@router.patch("/{notification_id}/read", response_model=NotificationResponse)
async def mark_single_as_read(
    notification_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    """
    Updates `is_read` boolean mapping selectively.
    """
    return await NotificationService.mark_as_read(db, current_user.id, notification_id)


@router.patch("/read-all", status_code=status.HTTP_200_OK)
async def mark_all_as_read(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    """
    Mass executes read toggles securely across full user bucket.
    """
    count = await NotificationService.mark_all_as_read(db, current_user.id)
    return {"message": f"{count} notifications successfully flagged as read."}


@router.delete("/{notification_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_notification(
    notification_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    """
    Deletes specific entity row explicitly ensuring cross-tenancy isolation.
    """
    await NotificationService.delete_notification(db, current_user.id, notification_id)


# ── Alerts Routing ──

@router.post("/alerts", status_code=status.HTTP_201_CREATED)
async def create_new_job_alert(
    data: JobAlertCreate,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    """
    Constructs new automated `JobAlert` queue logic evaluating specific structural properties dynamically inside the background execution thread.
    """
    alert = await NotificationService.create_job_alert(db, current_user.id, data)
    return {"message": "Job Alert active. The scheduler will dispatch matches natively.", "alert_id": alert.id}
