import fastapi
from starlette.responses import StreamingResponse
import schemas
from database.models import Documents
from database.engine import SessionDep
from sqlalchemy import select
from auth.jwt_handler import get_current_user
from fastapi import Depends, HTTPException, Form, File, UploadFile, Query
from io import BytesIO
from services.validate_user import validate_user, validate_admin

router = fastapi.APIRouter(
    prefix="/documents",
    tags=["Documents"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def get_documents(session: SessionDep,
                        current_user: str = Depends(get_current_user),
                        type_of_doc: str = Query(...)):
    user = await validate_user(current_user, session)
    stmt = select(Documents).where(Documents.type_of_document == type_of_doc)
    result = await session.execute(stmt)
    documents = result.scalars().all()

    return [
        {
            "id": d.id,
            "title": d.title,
            "description": d.description,
            "type_of_document": d.type_of_document,
            "date_of_uploaded": d.date_of_uploaded,
        }
        for d in documents
    ]


@router.get("/{document_id}/info")
async def get_document_info(document_id: int, session: SessionDep,
                            current_user: str = Depends(get_current_user)):
    user = await validate_user(current_user, session)

    stmt = select(Documents).where(Documents.id == document_id)
    execution = await session.execute(stmt)
    document = execution.scalar_one_or_none()
    if document is None:
        raise HTTPException(status_code=404, detail="Document not found")

    return {
        "id": document.id,
        "title": document.title,
        "description": document.description,
        "type_of_document": document.type_of_document,
        "date_of_uploaded": document.date_of_uploaded,
        "can_edit": user.role != "guest"
    }


@router.get("/{document_id}/download")
async def get_document(document_id: int, session: SessionDep,
                       current_user: str = Depends(get_current_user)):
    user = await validate_user(current_user, session)

    stmt = select(Documents).where(Documents.id == document_id)
    execution = await session.execute(stmt)
    document = execution.scalar_one_or_none()
    if document is None or not document.binary_data:
        raise HTTPException(status_code=404, detail="Document not found")

    file_like = BytesIO(document.binary_data)
    file_like.seek(0)
    return StreamingResponse(
        file_like,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": f"attachment; filename={document.title or 'document'}.docx"},
    )

@router.post("/")
async def create_document(
    session: SessionDep,
    title: str = Form(...),
    description: str = Form(None),
    type_of_document: str = Form(None),
    date_of_uploaded: str = Form(None),
    file: UploadFile = File(...),
    current_user: str = Depends(get_current_user)
):
    user = await validate_admin(current_user, session)
    binary_data = await file.read()
    doc = Documents(
        title=title,
        description=description,
        date_of_uploaded=date_of_uploaded,
        type_of_document=type_of_document,
        binary_data=binary_data
    )
    session.add(doc)
    await session.commit()
    await session.refresh(doc)
    return {
        "id": doc.id,
        "title": doc.title,
        "description": doc.description,
        "date_of_uploaded": doc.date_of_uploaded,
        "type_of_document": doc.type_of_document
    }

@router.post("/{document_id}")
async def update_document(
    document_id: int,
    session: SessionDep,
    title: str = Form(None),
    description: str = Form(None),
    type_of_document: str = Form(None),
    date_of_uploaded: str = Form(None),
    file: UploadFile = File(None),
    current_user: str = Depends(get_current_user)
):
    user = await validate_admin(current_user, session)
    
    stmt = select(Documents).where(Documents.id == document_id)
    execution = await session.execute(stmt)
    db_document = execution.scalar_one_or_none()

    if db_document is None:
        raise fastapi.HTTPException(status_code=404, detail="Document not found")
    if title is not None:
        db_document.title = title
    if description is not None:
        db_document.description = description
    if date_of_uploaded is not None:
        db_document.date_of_uploaded = date_of_uploaded
    if type_of_document is not None:
        db_document.type_of_document = type_of_document
    if file is not None:
        db_document.binary_data = await file.read()
    await session.commit()
    await session.refresh(db_document)
    return {
        "id": db_document.id,
        "title": db_document.title,
        "description": db_document.description,
        "date_of_uploaded": db_document.date_of_uploaded,
        "type_of_document": db_document.type_of_document
    }
