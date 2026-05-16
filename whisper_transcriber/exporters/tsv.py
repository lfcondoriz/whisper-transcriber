from whisper_transcriber.exporters.base import BaseExporter

class TSVExporter(BaseExporter):
    extension = "tsv"

    def format_content(self) -> str:
        # Agregamos la cabecera (header) del TSV
        blocks = ["start\tend\ttext"]
        
        for seg in self.segments:
            start = round(seg.start, 3)
            end = round(seg.end, 3)
            # Limpiamos el texto de posibles tabulaciones para no romper el formato
            text = seg.text.strip().replace("\t", " ")
            blocks.append(f"{start}\t{end}\t{text}")
            
        return "\n".join(blocks) + "\n"