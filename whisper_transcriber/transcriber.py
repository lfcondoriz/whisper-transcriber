from pathlib import Path
from faster_whisper import WhisperModel
from whisper_transcriber.config import Config
from whisper_transcriber.logger import setup_logger
from whisper_transcriber.utils import format_timestamp

logger = setup_logger()

def create_model(config: Config):
    return WhisperModel(
        config.model,
        device=config.device,
        compute_type=config.compute_type
    )


def transcribe_file(model, file_path: Path, output_dir: Path, config: Config):
    logger.info(f"Transcribing: {file_path.name}")

    segments, info = model.transcribe(
        str(file_path),
        language=config.language,
        task=config.task
    )

    segments = list(segments)

    # TXT
    text = "\n".join([seg.text for seg in segments])

    output_file = output_dir / f"{file_path.stem}.txt"

    output_file.write_text(text, encoding="utf-8")

    # SRT
    srt_file = output_dir / f"{file_path.stem}.srt"
    save_srt(segments, srt_file)

    logger.info(f"Saved: {output_file}")


def process_input_files(model, config: Config):
    input_dir = Path(config.input_dir)
    output_dir = Path(config.output_dir)

    output_dir.mkdir(parents=True, exist_ok=True)

    supported = {".mp3", ".mp4", ".wav", ".mkv", ".flac"}

    logger.info("Starting transcription pipeline")
    logger.info(f"Input dir: {input_dir}")
    logger.info(f"Output dir: {output_dir}")

    for file in input_dir.iterdir():
        if file.suffix.lower() in supported:
            logger.info(f"Processing file: {file.name}")
            transcribe_file(model, file, output_dir, config)

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