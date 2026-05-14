from faster_whisper import WhisperModel
from whisper_transcriber.config import Config


def create_model(config: Config):
    return WhisperModel(
        config.model,
        device=config.device,
        compute_type=config.compute_type
    )