from utils.pdf_processor import PDFProcessor


print(f"__name__ is: {__name__}")

if __name__ == "__main__":
    text = PDFProcessor.extract_text("sample.pdf")
    if text:
        print(f"Extracted {len(text)} characters")
        print(f"First 200 chars: {text[:200]}")
        
    text_2 = PDFProcessor.extract_text("sample_2.pdf")
    if text_2:
        print(f"Extracted {len(text_2)} characters")
        print(f"First 200 chars: {text_2[:200]}")