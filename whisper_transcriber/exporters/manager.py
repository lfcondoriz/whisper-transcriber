from whisper_transcriber.exporters.txt import TXTExporter
from whisper_transcriber.exporters.srt import SRTExporter
from pathlib import Path
from faster_whisper.transcribe import Segment


class ExportManager:
    def __init__(
            self, 
            segments: list[Segment], 
            output_dir: Path, 
            file_path: Path
        ) -> None:
            self.segments = segments
            self.output_dir = output_dir
            self.file_path = file_path

            self.exporters = [
                TXTExporter,
                SRTExporter
            ]

    def export_all(self) -> None:

        for exporter_cls in self.exporters:

            exporter = exporter_cls(
                self.segments,
                self.file_path
            )

            output_file = (
                self.output_dir /
                f"{self.file_path.stem}.{exporter.extension}"
            )

            exporter.save(output_file)