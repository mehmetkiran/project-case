import logging

import gridfs
from fastapi import Depends, APIRouter, HTTPException
from fastapi import UploadFile

from app.libs.exceptions.pdf import PDFException, InvalidPDFFormatException
from app.libs.hash import get_current_user
from app.libs.services.pdf import PDFService
from app.schemas.pdf import PDFSelectRequest
from db import client

logger = logging.getLogger(__name__)
router = APIRouter(
    prefix="/pdf",
    tags=["pdf"]
)

db = client["pdf_storage"]
fs = gridfs.GridFS(db)
metadata_collection = db["pdf_metadata"]


def get_pdf_service(
) -> PDFService:
    """FastAPI dependency to get an instance of PDFService."""
    return PDFService(db, fs)


@router.post("/pdf-upload/", response_model=None)
async def pdf_upload(file: UploadFile, pdf_service: PDFService = Depends(get_pdf_service),
                     current_user=Depends(get_current_user)):
    """
    Handles the uploading of a PDF file.
    The file is stored in GridFS, and its metadata is saved in the database.
    """

    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Only PDF files ('application/pdf') are accepted."
        )
    try:
        file_id = await pdf_service.upload_pdf(file, current_user.id)
        return {"message": "PDF successfully uploaded.", "file_id": file_id}
    except InvalidPDFFormatException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except PDFException as e:
        logging.error(f"PDF operation error for user {current_user.id}: {e.message}",
                      exc_info=False)
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        logging.critical(f"Unexpected error during PDF upload for user {current_user.id}: {e}",
                         exc_info=True)
        raise HTTPException(status_code=500, detail="An unexpected server error occurred.")


@router.get("/pdf-list/")
def pdf_list(pdf_service: PDFService = Depends(get_pdf_service),
             current_user=Depends(get_current_user)):
    """Retrieves a list of all PDFs uploaded by the currently authenticated user."""
    try:
        pdfs_data = pdf_service.list_pdfs_for_user(current_user.id)
        return {"pdf_list": pdfs_data}
    except PDFException as e:
        logging.error(f"Error listing PDFs for user {current_user.id}: {e.message}", exc_info=False)
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        logging.critical(f"Unexpected error listing PDFs for user {current_user.id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="An unexpected server error occurred.")


@router.post("/pdf-parse/")
async def pdf_parse(request: PDFSelectRequest, pdf_service: PDFService = Depends(get_pdf_service),
                    current_user=Depends(get_current_user)):
    """
      Parses the text content from a specified PDF belonging to the current user.
      The extracted text is stored in the database.
      """
    try:
        pdf_service.parse_pdf_text(request.pdf_id, current_user.id)
        return {
            "message": f"PDF '{request.pdf_id}' parsed successfully for user {current_user.id}."
        }
    except PDFException as e:
        logging.error(f"Error parsing PDF '{request.pdf_id}' for user {current_user.id}: {e.message}", exc_info=False)
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        logging.critical(f"Unexpected error parsing PDF '{request.pdf_id}' for user {current_user.id}: {e}",
                         exc_info=True)
        raise HTTPException(status_code=500, detail="An unexpected server error occurred.")


@router.post("/pdf-select/")
def pdf_select(request: PDFSelectRequest, pdf_service: PDFService = Depends(get_pdf_service),

               current_user=Depends(get_current_user)):
    """Marks a specific PDF as 'selected' for the currently authenticated user."""
    try:
        pdf_service.select_pdf_for_user(request.pdf_id, current_user.id)
        return {"message": f"PDF '{request.pdf_id}' selected successfully for user {current_user.id}."}
    except PDFException as e:
        logging.error(f"Error selecting PDF '{request.pdf_id}' for user {current_user.id}: {e.message}", exc_info=False)
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        logging.critical(f"Unexpected error selecting PDF '{request.pdf_id}' for user {current_user.id}: {e}",
                         exc_info=True)
        raise HTTPException(status_code=500, detail="An unexpected server error occurred.")
