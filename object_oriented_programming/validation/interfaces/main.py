from pathlib import Path

from abstract import FileReaderInterface

BASE_DIR: Path = Path(__file__).parent.resolve()


class PdfReader(FileReaderInterface):
    """Concrete implementation of FileReaderInterface for PDF files."""

    def load_file(self, file_path: Path) -> str:
        # Implementation for loading a PDF file
        return f"Loading PDF file from {file_path}"

    def extract_text(self) -> str:
        # Implementation for extracting text from a PDF file
        return "Extracted text from PDF"


class DocxReader(FileReaderInterface):
    """Concrete implementation of FileReaderInterface for DOCX files."""

    def load_file(self, file_path: Path) -> str:
        # Implementation for loading a DOCX file
        return f"Loading DOCX file from {file_path}"

    def extract_text(self) -> str:
        # Implementation for extracting text from a DOCX file
        return "Extracted text from DOCX"


def main() -> None:
    pdf_reader = PdfReader()
    docx_reader = DocxReader()

    pdf_file_path: Path = BASE_DIR / "sample.pdf"
    docx_file_path: Path = BASE_DIR / "sample.docx"

    print(pdf_reader.load_file(file_path=pdf_file_path))
    print(pdf_reader.extract_text())

    print(docx_reader.load_file(file_path=docx_file_path))
    print(docx_reader.extract_text())


if __name__ == "__main__":
    main()
