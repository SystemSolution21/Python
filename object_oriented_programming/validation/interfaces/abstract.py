from abc import ABC, abstractmethod
from pathlib import Path


class FileReaderInterface(ABC):
    """Interface for file readers."""

    @abstractmethod
    def load_file(self, file_path: Path) -> str:
        """
        Load the file for text extraction. This method should be implemented by subclasses to handle the specific file format.
        """
        pass

    @abstractmethod
    def extract_text(self) -> str:
        """
        Extract text from the loaded file. This method should be implemented by subclasses to handle the specific file format.
        """
        pass
