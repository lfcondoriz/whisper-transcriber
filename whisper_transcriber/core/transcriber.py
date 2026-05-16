from pathlib import Path
from faster_whisper import WhisperModel
from whisper_transcriber.config import Config
from whisper_transcriber.exporters.manager import ExportManager
from whisper_transcriber.logger import setup_logger
import time

logger = setup_logger()


class WhisperTranscriber:
    """Servicio principal para manejar las transcripciones con Faster-Whisper."""
    
    SUPPORTED_FORMATS = {".mp3", ".mp4", ".wav", ".mkv", ".flac", ".webm"}

    def __init__(self, config: Config):
        self.config = config
        self.input_dir = Path(config.input_dir)
        self.output_dir = Path(config.output_dir)
        
        # Inicializamos el modelo al instanciar la clase
        logger.info(f"Loading Whisper model '{config.model}' on {config.device}...")
        self.model = WhisperModel(
            model_size_or_path=config.model,
            device=config.device,
            compute_type=config.compute_type
        )

    def _is_already_processed(self, file_path: Path) -> bool:
        """
        Comprueba si todos los formatos de salida solicitados 
        ya existen para un archivo específico.
        """
        for fmt in self.config.formats:
            expected_output_file = self.output_dir / f"{file_path.stem}.{fmt}"
            # Si falta al menos uno de los formatos, necesitamos procesarlo
            if not expected_output_file.exists():
                return False
        
        # Si termina el bucle, significa que todos los archivos ya existen
        return True

    def transcribe_file(self, file_path: Path) -> None:

        if self._is_already_processed(file_path):
            logger.info(f"Skipped: {file_path.name} (Already processed)")
            return

        logger.info(f"Transcribing: {file_path.name}")

        start_time = time.time()

        segments_generator, info = self.model.transcribe(
            str(file_path),
            language=self.config.language,
            task=self.config.task,
            beam_size=1,
            vad_filter=False,
            condition_on_previous_text=False,
        )

        total_duration = info.duration
        segments = []

        last_logged_progress = 0

        for segment in segments_generator:

            segments.append(segment)

            progress = (segment.end / total_duration) * 100 if total_duration else 0

            elapsed = time.time() - start_time
            
            if segment.end > 5:
                eta = (elapsed / segment.end) * (total_duration - segment.end)
            else:
                eta = 0

            if self.config.verbose:
                logger.info(
                    f"[{progress:5.1f}%] "
                    f"{segment.end:7.1f}s / {total_duration:7.1f}s | "
                    f"ETA {eta:6.1f}s | "
                    f"{segment.text.strip()}"
                )
            else:
                if progress - last_logged_progress > 10:
                    logger.info(
                        f"[{progress:5.1f}%] "
                        f"{segment.end:7.1f}s / {total_duration:7.1f}s"
                    )
                    last_logged_progress = progress

        export_manager = ExportManager(
            segments=segments,
            output_dir=self.output_dir,
            file_path=file_path,
            formats=self.config.formats
        )

        export_manager.export_all()

        logger.info(f"Saved: {file_path.name} in {self.output_dir}")

    def process_all(self) -> None:
        """Procesa todos los archivos en el directorio de entrada."""
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info("Starting transcription pipeline...")
        
        # Iteramos y validamos
        files_to_process = [
            f for f in self.input_dir.iterdir() 
            if f.is_file() and f.suffix.lower() in self.SUPPORTED_FORMATS
        ]

        if not files_to_process:
            logger.warning(f"No supported media files found in {self.input_dir}")
            return

        for file_path in files_to_process:
            self.transcribe_file(file_path)
            
        logger.info("Pipeline finished successfully.")