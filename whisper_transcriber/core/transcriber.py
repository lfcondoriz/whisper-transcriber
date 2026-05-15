from pathlib import Path
from whisper_transcriber.exporters.manager import ExportManager
from whisper_transcriber.logger import setup_logger

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

    export_manager = ExportManager(
        segments=segments,
        output_dir=output_dir,
        file_path=file_path
    )

    export_manager.export_all()

    logger.info(f"Saved: {file_path.name} in {output_dir}")


def process_input_files(model, config):
    input_dir = Path(config.input_dir)
    output_dir = Path(config.output_dir)

    output_dir.mkdir(parents=True, exist_ok=True)

    logger.info("Starting pipeline")

    for file_path  in input_dir.iterdir():
        if file_path .suffix.lower() in SUPPORTED:
            transcribe_file(model,  file_path, output_dir, config)