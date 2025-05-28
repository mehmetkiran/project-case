import io
from datetime import datetime, timezone
from typing import List, Dict, Any

from PyPDF2 import PdfReader
from bson import ObjectId
from gridfs import GridFS
from gridfs.errors import NoFile
from pymongo.database import Database
from pymongo.collection import Collection
from fastapi import UploadFile

from app.libs.exceptions.pdf import InvalidPDFFormatException, DatabaseOperationException, PDFNotFoundException, \
    PDFParsingException, NoTextExtractedException


class PDFService:
    """
    Service class for handling PDF-related business logic.
    This includes uploading, listing, parsing, and selecting PDFs.
    """
    def __init__(self, db: Database, fs: GridFS):
        """
        Initializes the PDFService.

        Args:
            db: A PyMongo Database instance.
            fs: A GridFS instance.
        """
        self.db = db
        self.fs = fs
        self.metadata_collection: Collection = db.pdf_metadata
        self.user_pdf_parser_collection: Collection = db.user_pdf_parser
        self.user_pdf_selection_collection: Collection = db.user_pdf_selection

    async def upload_pdf(self, file: UploadFile, user_id: int) -> str:
        """
        Uploads a PDF file to GridFS and saves its metadata.

        Args:
            file: The UploadFile object from FastAPI.
            user_id: The ID of the user uploading the file.

        Returns:
            The GridFS file ID as a string.

        Raises:
            InvalidPDFFormatException: If the uploaded file is empty.
            DatabaseOperationException: If there's an error with GridFS or metadata saving.
        """
        contents = await file.read()
        if not contents:
            raise InvalidPDFFormatException("Uploaded file cannot be empty.")

        try:
            file_id_obj: ObjectId = self.fs.put(
                contents,
                filename=file.filename,
                user_id=str(user_id),
                content_type=file.content_type
            )
        except Exception as e:
            raise DatabaseOperationException(f"Error uploading file to GridFS: {e}")

        file_id_str = str(file_id_obj)
        metadata = {
            "user_id": user_id,
            "filename": file.filename,
            "upload_date": datetime.now(timezone.utc),
            "gridfs_id": file_id_str,
            "content_type": file.content_type
        }
        try:
            self.metadata_collection.insert_one(metadata)
        except Exception as e:
            self.fs.delete(file_id_obj)
            raise DatabaseOperationException(f"Error saving PDF metadata: {e}")

        return file_id_str

    def list_pdfs_for_user(self, user_id: int) -> List[Dict[str, Any]]:
        """
        Lists all PDFs uploaded by a specific user.

        Args:
            user_id: The ID of the user.

        Returns:
            A list of dictionaries, each representing a PDF's metadata.

        Raises:
            DatabaseOperationException: If there's an error querying the database.
        """
        try:
            pdf_cursor = self.metadata_collection.find({"user_id": user_id})
            result = []
            for pdf in pdf_cursor:
                upload_date = pdf.get("upload_date")
                result.append({
                    "filename": pdf.get("filename"),
                    "upload_date": upload_date.isoformat() if upload_date else None,
                    "file_id": pdf.get("gridfs_id")
                })
            return result
        except Exception as e:
            raise DatabaseOperationException(f"Error retrieving PDF list for user {user_id}: {e}")

    def _get_pdf_metadata_and_validate_user(self, pdf_id_str: str, user_id: int) -> Dict[str, Any]:
        """
        Helper function to retrieve PDF metadata and validate user ownership.

        Args:
            pdf_id_str: The GridFS ID of the PDF (as a string).
            user_id: The ID of the user.

        Returns:
            The PDF metadata document.

        Raises:
            InvalidPDFFormatException: If the pdf_id_str has an invalid format.
            PDFNotFoundException: If the PDF is not found for the given user.
        """
        try:
            ObjectId(pdf_id_str) # Validate ID format
        except Exception:
            raise InvalidPDFFormatException(f"Invalid PDF ID format: {pdf_id_str}")

        pdf_doc = self.metadata_collection.find_one({
            "user_id": user_id,
            "gridfs_id": pdf_id_str
        })
        if not pdf_doc:
            raise PDFNotFoundException(
                f"PDF with ID '{pdf_id_str}' not found for user {user_id} or unauthorized access."
            )
        return pdf_doc

    def _get_pdf_bytes_from_gridfs(self, gridfs_id_str: str) -> bytes:
        """
        Helper function to retrieve PDF content (bytes) from GridFS.

        Args:
            gridfs_id_str: The GridFS ID of the PDF (as a string).

        Returns:
            The PDF content as bytes.

        Raises:
            PDFNotFoundException: If the file is not found in GridFS.
            DatabaseOperationException: For other GridFS or ObjectId errors.
        """
        try:
            object_id = ObjectId(gridfs_id_str)
            grid_out = self.fs.get(object_id)
            pdf_bytes = grid_out.read()
            return pdf_bytes
        except NoFile:
            raise PDFNotFoundException(f"PDF file with GridFS ID '{gridfs_id_str}' not found in GridFS.")
        except Exception as e:
            raise DatabaseOperationException(f"Error reading PDF from GridFS (ID: {gridfs_id_str}): {e}")

    def parse_pdf_text(self, pdf_id_str: str, user_id: int) -> str:
        """
        Parses text from a PDF file.

        Args:
            pdf_id_str: The GridFS ID of the PDF to parse.
            user_id: The ID of the user requesting the parsing.

        Returns:
            The extracted text content as a string.

        Raises:
            PDFNotFoundException: If the PDF metadata or file is not found.
            InvalidPDFFormatException: If the PDF has no pages or is malformed.
            PDFParsingException: If text extraction fails.
            NoTextExtractedException: If no text is found in the PDF.
            DatabaseOperationException: If saving parsed text fails.
        """
        self._get_pdf_metadata_and_validate_user(pdf_id_str, user_id) # Validates existence and ownership
        pdf_bytes = self._get_pdf_bytes_from_gridfs(pdf_id_str)

        pdf_stream = io.BytesIO(pdf_bytes)
        try:
            reader = PdfReader(pdf_stream)
            if not reader.pages:
                 raise InvalidPDFFormatException("PDF file does not contain any pages.")
        except Exception as e:
            raise PDFParsingException(f"Could not initialize PDF reader or file is unreadable (ID: {pdf_id_str}): {e}")

        full_text = ""
        for i, page in enumerate(reader.pages):
            try:
                text = page.extract_text()
                if text:
                    full_text += text + "\n"
            except Exception as e:
                raise PDFParsingException(f"Error parsing page {i+1} of PDF (ID: {pdf_id_str}): {e}")

        if not full_text.strip():
            raise NoTextExtractedException(f"No text could be extracted from PDF (ID: {pdf_id_str}).")

        try:
            self.user_pdf_parser_collection.update_one(
                {"user_id": user_id, "source_pdf_id": pdf_id_str},
                {"$set": {
                    "text_content": full_text,
                    "last_parsed_at": datetime.now(timezone.utc)
                    }
                },
                upsert=True
            )
        except Exception as e:
            raise DatabaseOperationException(f"Error saving parsed text for PDF (ID: {pdf_id_str}): {e}")

        return full_text

    def select_pdf_for_user(self, pdf_id_str: str, user_id: int) -> None:
        """
        Marks a PDF as selected for a user.

        Args:
            pdf_id_str: The GridFS ID of the PDF to select.
            user_id: The ID of the user.

        Raises:
            PDFNotFoundException: If the PDF is not found for the user.
            DatabaseOperationException: If saving the selection fails.
        """
        pdf_doc = self._get_pdf_metadata_and_validate_user(pdf_id_str, user_id)

        try:
            self.user_pdf_selection_collection.update_one(
                {"user_id": user_id},
                {"$set": {
                    "selected_pdf_id": pdf_id_str,
                    "selected_filename": pdf_doc.get("filename"), # Store filename for convenience
                    "selection_date": datetime.now(timezone.utc)
                    }
                },
                upsert=True
            )
        except Exception as e:
            raise DatabaseOperationException(f"Error saving PDF selection for user {user_id}, PDF ID {pdf_id_str}: {e}")