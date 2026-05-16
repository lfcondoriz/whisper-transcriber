from abc import ABC, abstractmethod
from pathlib import Path
from faster_whisper.transcribe import Segment


class BaseExporter(ABC):
    extension: str = ""

    def __init__(
        self,
        segments: list[Segment],
        file_path: Path,
    ) -> None:
        self.segments = segments
        self.file_path = file_path

    @abstractmethod
    def format_content(self) -> str:
        pass

    def save(self, output_file: Path) -> Path:
        output_file.parent.mkdir(parents=True, exist_ok=True)

        output_file.write_text(
            self.format_content(),
            encoding="utf-8"
        )

        return output_file
    
    def format_time(self, seconds: float, separator: str = ",") -> str:
            """
            Convierte segundos a HH:MM:SS,MMM. 
            Permite cambiar el separador (coma para SRT, punto para VTT).
            """
            hours = int(seconds // 3600)
            minutes = int((seconds % 3600) // 60)
            secs = int(seconds % 60)
            milliseconds = int((seconds - int(seconds)) * 1000)
            
            return f"{hours:02}:{minutes:02}:{secs:02}{separator}{milliseconds:03}"