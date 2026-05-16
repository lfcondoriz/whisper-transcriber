import argparse


def parse_args():
    parser = argparse.ArgumentParser(
        description="Whisper Transcriber CLI"
    )

    parser.add_argument(
        "--model",
        type=str,
        default="base",
        help="Whisper model size (tiny, base, small, medium, large)"
    )

    parser.add_argument(
        "--device",
        type=str,
        default="cuda",
        help="Device to run inference on (cpu or cuda)"
    )

    parser.add_argument(
        "--compute_type",
        type=str,
        default="float16",
        help="Compute type for model (float32 (high precision), float16 (mixed precision), int8 (quantized))"
    )

    parser.add_argument(
        "--language",
        type=str,
        default=None,
        help="Language code (e.g. 'es', 'en'). Use None for auto-detect"
    )

    parser.add_argument(
        "--task",
        type=str,
        default="transcribe",
        choices=["transcribe", "translate"],
        help="Task mode: transcribe (same language) or translate (to English)"
    )    

    parser.add_argument(
        "--input",
        type=str,
        default="data/input",
        help="Input directory with media files"
    )

    parser.add_argument(
        "--output",
        type=str,
        default="data/output",
        help="Output directory for transcripts"
    )

    parser.add_argument(
        "--formats",
        type=str,
        nargs="+", # Permite múltiples valores ej: --formats txt srt vtt
        choices=["txt", "srt", "vtt", "json", "tsv"],
        default=["txt", "srt"], # Si no pone nada, da estos por defecto
        help="Output formats to generate. Default: txt srt"
    )
    
    return parser.parse_args()