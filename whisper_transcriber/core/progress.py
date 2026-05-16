import time
from typing import Iterable
from faster_whisper.transcribe import Segment
from whisper_transcriber.logger import setup_logger

logger = setup_logger()

class ProgressTracker:
    """Se encarga de calcular el ETA y registrar el progreso de la transcripción."""
    
    def __init__(self, total_duration: float, verbose: bool):
        self.total_duration = total_duration
        self.verbose = verbose
        self.start_time = time.time()
        self.last_logged_progress = 0

    def track(self, segments_generator: Iterable[Segment]) -> list[Segment]:
        """Itera el generador, emite los logs y devuelve la lista de segmentos."""
        segments = []
        for segment in segments_generator:
            segments.append(segment)
            self._log_progress(segment)
            
        return segments

    def _log_progress(self, segment: Segment) -> None:
        if not self.total_duration:
            return

        progress = (segment.end / self.total_duration) * 100
        elapsed = time.time() - self.start_time
        
        eta = 0.0
        if segment.end > 5:
            eta = (elapsed / segment.end) * (self.total_duration - segment.end)

        if self.verbose:
            logger.info(
                f"[{progress:5.1f}%] "
                f"{segment.end:7.1f}s / {self.total_duration:7.1f}s | "
                f"ETA {eta:6.1f}s | "
                f"{segment.text.strip()}"
            )
        elif progress - self.last_logged_progress > 10:
            # Modo no verboso: loguea cada 10%
            logger.info(
                f"[{progress:5.1f}%] "
                f"{segment.end:7.1f}s / {self.total_duration:7.1f}s"
            )
            self.last_logged_progress = progress