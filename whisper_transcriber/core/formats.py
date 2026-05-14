from pathlib import Path
from whisper_transcriber.utils import format_timestamp


def save_srt(segments, output_file: Path):
    lines = []

    for i, seg in enumerate(segments, start=1):
        start = format_timestamp(seg.start)
        end = format_timestamp(seg.end)

        lines.append(str(i))
        lines.append(f"{start} --> {end}")
        lines.append(seg.text.strip())
        lines.append("")

    output_file.write_text("\n".join(lines), encoding="utf-8")