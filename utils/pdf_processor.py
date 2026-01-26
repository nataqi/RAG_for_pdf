from typing import Optional
import PyPDF2
import logging



logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PDFProcessor:
    """Handles PDF text extraction"""
    
    @staticmethod
    def extract_text(file_path: str) -> Optional[str]:
        """
            Extract text from a PDF file.

            Args:
                file_path: Path to the PDF file
            Returns:
                Extracted text as string, or None if extraction fails
        """
        
        try:
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                
                for page in reader.pages:
                    page_text = page.extract_text()
                    text += page_text + "\n"
                
                if not text.strip():
                    logger.warning(f"No text extracted from {file_path}. This may be a scanned PDF (image-based) or empty document.")
                    return None
        
                logger.info(f"Successfully extracted {len(text)} characters from {file_path}")
                return text
        
        except Exception as e:
            logger.error(f"Error extracting text from {file_path}: {e}")
            return None
                