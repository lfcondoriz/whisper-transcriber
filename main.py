from faster_whisper import WhisperModel

model = WhisperModel(
    "large-v3",
    device="cuda",
    compute_type="float16"
)

segments, info = model.transcribe(
    "data/input/videoplayback.mp4",
    beam_size=5
)

print("Idioma:", info.language)
print("Probabilidad:", info.language_probability)

for segment in segments:
    print(f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}")