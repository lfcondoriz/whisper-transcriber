from pathlib import Path
from whisper_transcriber.logger import setup_logger
from whisper_transcriber.core.formats import save_srt

logger = setup_logger()

SUPPORTED = {".mp3", ".mp4", ".wav", ".mkv", ".flac"}


def transcribe_file(model, file_path: Path, output_dir: Path, config):
    logger.info(f"Transcribing: {file_path.name}")

    segments, _ = model.transcribe(
        str(file_path),
        language=config.language,
        task=config.task
    )

    segments = list(segments)

    text = "\n".join(seg.text for seg in segments)

    txt_file = output_dir / f"{file_path.stem}.txt"
    txt_file.write_text(text, encoding="utf-8")

    srt_file = output_dir / f"{file_path.stem}.srt"
    save_srt(segments, srt_file)

    logger.info(f"Saved: {txt_file}")


def process_input_files(model, config):
    input_dir = Path(config.input_dir)
    output_dir = Path(config.output_dir)

    output_dir.mkdir(parents=True, exist_ok=True)

    logger.info("Starting pipeline")

    for file in input_dir.iterdir():
        if file.suffix.lower() in SUPPORTED:
            transcribe_file(model, file, output_dir, config)