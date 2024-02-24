from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import models
from database import get_database
from error_handlers.DataError import DataException
from error_handlers.UserError import UserException
from schemas.NoteSchemas import NoteSchema, NoteID, NoteUpdate
from schemas.UserSchemas import UserID
from utils import validate_api_key
from datetime import datetime


router = APIRouter(prefix='/api/notes', tags=['Note endpoints'])


@router.get('/')
async def root(api_key: str = Depends(validate_api_key), db: Session = Depends(get_database)):
    note_data = db.query(models.Note).all()

    if not note_data:
        return JSONResponse(status_code=200, content={'message': 'No notes found'})

    return note_data


@router.post('/')
async def create_note(user_id: UserID, note: NoteSchema, api_key: str = Depends(validate_api_key), db: Session = Depends(get_database)):
    user = db.query(models.User).filter_by(id=user_id.id).first()

    if not user:
        raise UserException(status_code=status.HTTP_400_BAD_REQUEST, details='User not found')

    note_model = models.Note()
    note_model.title = note.title
    note_model.content = note.content
    note_model.owner_id = user_id.id

    db.add(note_model)
    db.commit()
    db.refresh(note_model)

    return note_model


@router.put("/{note_id}")
async def update_note(note_id: str, note_data: NoteUpdate, api_key: str = Depends(validate_api_key),
                      db: Session = Depends(get_database)):
    note = db.query(models.Note).filter_by(id=note_id).first()

    if not note:
        raise DataException(status_code=status.HTTP_400_BAD_REQUEST, details='Note not found')

    note.title = note_data.title
    note.content = note_data.content
    note.updated_at = datetime.now()

    db.commit()
    db.refresh(note)

    return note


@router.delete('/')
async def delete_note(note_id: NoteID, api_key: str = Depends(validate_api_key), db: Session = Depends(get_database)):
    note = db.query(models.Note).filter_by(id=note_id.id).first()

    if not note:
        raise DataException(status_code=status.HTTP_400_BAD_REQUEST, details='Note not found')

    db.delete(note)
    db.commit()

    return {'response': 'Successfully deleted note', 'note_id': note.id}


@router.get('/owner')
async def get_notes_for_owner(user_id: UserID, api_key: str = Depends(validate_api_key),
                              db: Session = Depends(get_database)):
    user = db.query(models.User).filter_by(id=user_id.id).first()

    if not user:
        raise UserException(status_code=400, details='User does not exist')

    notes = db.query(models.Note).filter_by(owner_id=user_id.id).all()

    if not notes:
        return JSONResponse(status_code=201, content={'response': 'User ' + user_id.id + ' has no notes'})

    return {'response': 'Successfully retrieved notes for owner', 'data': notes}
