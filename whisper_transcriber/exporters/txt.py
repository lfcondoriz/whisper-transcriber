from whisper_transcriber.exporters.base import BaseExporter
from pathlib import Path

class TXTExporter(BaseExporter):
    extension = "txt"

    def format_content(self) -> str:
        return "\n".join(seg.text.strip() for seg in self.segments)