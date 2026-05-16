import json
from whisper_transcriber.exporters.base import BaseExporter

class JSONExporter(BaseExporter):
    extension = "json"

    def format_content(self) -> str:
        # Extraemos los datos útiles de cada Segment a una lista de diccionarios
        data = [
            {
                "start": round(seg.start, 3),
                "end": round(seg.end, 3),
                "text": seg.text.strip()
            }
            for seg in self.segments
        ]
        
        # ensure_ascii=False evita que los acentos se guarden como \u00f3
        return json.dumps(data, indent=4, ensure_ascii=False)