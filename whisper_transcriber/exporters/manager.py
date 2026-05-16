from pathlib import Path
from faster_whisper.transcribe import Segment

from whisper_transcriber.exporters.base import BaseExporter
from whisper_transcriber.exporters.txt import TXTExporter
from whisper_transcriber.exporters.srt import SRTExporter
from whisper_transcriber.exporters.vtt import VTTExporter
from whisper_transcriber.exporters.json import JSONExporter
from whisper_transcriber.exporters.tsv import TSVExporter

# Diccionario que conecta el texto del CLI con la clase real
EXPORTERS_REGISTRY = {
    "txt": TXTExporter,
    "srt": SRTExporter,
    "vtt": VTTExporter,
    "json": JSONExporter,
    "tsv": TSVExporter
}

class ExportManager:
    def __init__(
            self, 
            segments: list[Segment], 
            output_dir: Path, 
            file_path: Path,
            formats: list[str] = None
        ) -> None:
            self.segments = segments
            self.output_dir = output_dir
            self.file_path = file_path
            self.formats = formats or ["txt", "srt"]

    def export_all(self) -> None:
        for fmt in self.formats:
            # Buscamos la clase en el diccionario
            exporter_cls = EXPORTERS_REGISTRY.get(fmt)
            
            if not exporter_cls:
                continue # Ignora silenciosamente si el formato no existe
                
            # Instanciamos y guardamos
            exporter = exporter_cls(self.segments, self.file_path)
            output_file = self.output_dir / f"{self.file_path.stem}.{exporter.extension}"
            exporter.save(output_file)