from whisper_transcriber.exporters.base import BaseExporter


class SRTExporter(BaseExporter):
    extension = "srt"

    def format_content(self) -> str:
        srt_content = ""
        for i, seg in enumerate(self.segments, start=1):
            start_time = self.format_time(seg.start)
            end_time = self.format_time(seg.end)
            srt_content += f"{i}\n{start_time} --> {end_time}\n{seg.text}\n\n"
        return srt_content

    @staticmethod
    def format_time(seconds: float) -> str:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        milliseconds = int((seconds - int(seconds)) * 1000)
        return f"{hours:02}:{minutes:02}:{secs:02},{milliseconds:03}"