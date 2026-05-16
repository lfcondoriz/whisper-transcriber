from pathlib import Path
from faster_whisper import WhisperModel
from whisper_transcriber.config import Config
from whisper_transcriber.exporters.manager import ExportManager
from whisper_transcriber.logger import setup_logger

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

    def transcribe_file(self, file_path: Path) -> None:
        """Transcribe un solo archivo y delega la exportación."""
        logger.info(f"Transcribing: {file_path.name}")

        # Ya no necesitamos pasar el modelo o el config, están en 'self'
        segments_generator, _ = self.model.transcribe(
            str(file_path),
            language=self.config.language,
            task=self.config.task
        )

        segments = list(segments_generator)

        # Usamos el manager refactorizado del paso anterior
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