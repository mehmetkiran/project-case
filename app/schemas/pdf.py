from pydantic import BaseModel


class PDFSelectRequest(BaseModel):
    pdf_id: str
