from whisper_transcriber.exporters.base import BaseExporter

class VTTExporter(BaseExporter):
    extension = "vtt"

    def format_content(self) -> str:
        # VTT siempre debe empezar con esta cabecera
        blocks = ["WEBVTT"]
        
        for seg in self.segments:
            # Sobrescribimos el separador para usar el punto
            start_time = self.format_time(seg.start, separator=".")
            end_time = self.format_time(seg.end, separator=".")
            
            blocks.append(f"{start_time} --> {end_time}\n{seg.text.strip()}")
            
        return "\n\n".join(blocks) + "\n\n"