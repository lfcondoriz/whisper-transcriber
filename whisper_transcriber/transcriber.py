from pathlib import Path

from faster_whisper import WhisperModel


INPUT_DIR = Path("data/input")
OUTPUT_DIR = Path("data/output")


model = WhisperModel(
    "base",
    device="cpu",
    compute_type="int8"
)


def transcribe_file(file_path: Path) -> None:
    print(f"Transcribing: {file_path.name}")

    segments, info = model.transcribe(str(file_path))

    transcription = []

    for segment in segments:
        transcription.append(segment.text)

    output_file = OUTPUT_DIR / f"{file_path.stem}.txt"

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(transcription))

    print(f"Saved: {output_file}")


def process_input_files() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    supported_extensions = [
        ".mp3",
        ".wav",
        ".mp4",
        ".mkv",
        ".flac",
    ]

    for file_path in INPUT_DIR.iterdir():
        if file_path.suffix.lower() in supported_extensions:
            transcribe_file(file_path)