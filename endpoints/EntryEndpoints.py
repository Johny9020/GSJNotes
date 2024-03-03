from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session, defer
from database import get_database
import models
from fastapi.encoders import jsonable_encoder
from schemas.EntrySchemas import DiaryEntryCreate, NotificationCreate
from utils import validate_api_key

router = APIRouter(prefix='/api/entry', tags=['Entry Endpoints'])


@router.get('')
async def get_entries(api_key: str = Depends(validate_api_key), db: Session = Depends(get_database)):
    entries = db.query(models.DiaryEntry).all()

    if not entries:
        return JSONResponse(status_code=200, content={'message': 'There are no entries in the database'})

    return entries


@router.get('/notifications')
async def get_notifications(api_key: str = Depends(validate_api_key), db: Session = Depends(get_database)):
    notifications = db.query(models.NotificationModel).all()

    if not notifications:
        return JSONResponse(status_code=200, content={'message': 'There are no notifications in the database'})

    return notifications


@router.get('/{entry_id}')
async def get_entry(entry_id: str, api_key: str = Depends(validate_api_key), db: Session = Depends(get_database)):
    entry = db.query(models.DiaryEntry).filter_by(id=entry_id).first()
    notifications = (db.query(models.NotificationModel).options(defer(models.NotificationModel.diary_entry_id))
                     .filter_by(diary_entry_id=entry_id).all())

    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")

    json_data = jsonable_encoder(entry)

    if notifications:
        json_data.update({'notifications': notifications})

    return json_data


@router.post('/create')
async def index(entry: DiaryEntryCreate, api_key: str = Depends(validate_api_key), db: Session = Depends(get_database)):
    if not entry:
        return JSONResponse(status_code=400, content={'message': 'No'})

    diary_entry = models.DiaryEntry()
    diary_entry.title = entry.title
    diary_entry.content = entry.content

    db.add(diary_entry)
    db.commit()
    db.refresh(diary_entry)

    return diary_entry


@router.post("/{entry_id}/notifications/")
async def create_notification_for_entry(entry_id: str, notification: NotificationCreate,
                                        api_key: str = Depends(validate_api_key), db: Session = Depends(get_database)):
    entry = db.query(models.DiaryEntry).filter_by(id=entry_id).first()

    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")

    db_notification = models.NotificationModel()
    db_notification.diary_entry_id = entry_id
    db_notification.due_date = notification.due_date

    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    db.refresh(entry)

    return db_notification


@router.delete('/{entry_id}')
async def delete_entry(entry_id: str, db: Session = Depends(get_database)):
    entry = db.query(models.DiaryEntry).filter_by(id=entry_id).first()

    if not entry:
        raise HTTPException(status_code=400, detail="Entry not found")

    db.delete(entry)
    db.commit()

    return {
        "success": True
    }


@router.delete('/notifications/{notification_id}')
async def delete_entry(notification_id: str, db: Session = Depends(get_database)):
    notification = db.query(models.NotificationModel).filter_by(id=notification_id).first()

    if not notification:
        raise HTTPException(status_code=400, detail="Notification not found")

    db.delete(notification)
    db.commit()

    return {
        "success": True
    }
