from pathlib import Path
from faster_whisper import WhisperModel
from whisper_transcriber.config import Config


def create_model(config: Config):
    return WhisperModel(
        config.model,
        device=config.device,
        compute_type=config.compute_type
    )


def transcribe_file(model, file_path: Path, output_dir: Path):
    print(f"Transcribing: {file_path.name}")

    segments, _ = model.transcribe(str(file_path))

    text = "\n".join([seg.text for seg in segments])

    output_file = output_dir / f"{file_path.stem}.txt"

    output_file.write_text(text, encoding="utf-8")

    print(f"Saved: {output_file}")


def process_input_files(model, config: Config):
    input_dir = Path(config.input_dir)
    output_dir = Path(config.output_dir)

    output_dir.mkdir(parents=True, exist_ok=True)

    supported = {".mp3", ".mp4", ".wav", ".mkv", ".flac"}

    for file in input_dir.iterdir():
        if file.suffix.lower() in supported:
            transcribe_file(model, file, output_dir)