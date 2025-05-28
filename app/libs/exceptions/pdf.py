# app/exceptions.py

class PDFException(Exception):
    """Base exception class for PDF related errors."""
    def __init__(self, message: str = "A PDF error occurred.", status_code: int = 500):
        """
        Args:
            message: The error message.
            status_code: The HTTP status code to associate with this error.
        """
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class PDFNotFoundException(PDFException):
    """Exception raised when a PDF is not found."""
    def __init__(self, message: str = "PDF not found.", pdf_id: str | None = None):
        """
        Args:
            message: The error message.
            pdf_id: The ID of the PDF that was not found (optional).
        """
        super().__init__(message, status_code=404)
        self.pdf_id = pdf_id

class InvalidPDFFormatException(PDFException):
    """Exception raised for invalid PDF format or content."""
    def __init__(self, message: str = "Invalid PDF format or content."):
        """
        Args:
            message: The error message.
        """
        super().__init__(message, status_code=400)

class PDFParsingException(PDFException):
    """Exception raised when PDF parsing fails."""
    def __init__(self, message: str = "Failed to parse PDF."):
        """
        Args:
            message: The error message.
        """
        super().__init__(message, status_code=422)

class NoTextExtractedException(PDFException):
    """Exception raised when no text can be extracted from a PDF."""
    def __init__(self, message: str = "No text could be extracted from the PDF."):
        """
        Args:
            message: The error message.
        """
        super().__init__(message, status_code=400)

class DatabaseOperationException(PDFException):
    """Exception raised for errors during database operations."""
    def __init__(self, message: str = "A database operation error occurred."):
        """
        Args:
            message: The error message.
        """
        super().__init__(message, status_code=500)