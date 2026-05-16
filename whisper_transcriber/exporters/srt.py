from whisper_transcriber.exporters.base import BaseExporter

class SRTExporter(BaseExporter):
    extension = "srt"

    def format_content(self) -> str:
        blocks = []
        for i, seg in enumerate(self.segments, start=1):
            # Usamos el formateador heredado de BaseExporter (usa ',' por defecto)
            start_time = self.format_time(seg.start)
            end_time = self.format_time(seg.end)
            
            blocks.append(f"{i}\n{start_time} --> {end_time}\n{seg.text.strip()}")
            
        return "\n\n".join(blocks) + "\n\n"