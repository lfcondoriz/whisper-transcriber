import argparse


def parse_args():

    parser = argparse.ArgumentParser(
        prog="whisper_transcriber",
        description="Fast batch audio/video transcription using faster-whisper.",
        epilog="""
            Examples:
            python -m whisper_transcriber --language es
            python -m whisper_transcriber --model large-v3
            python -m whisper_transcriber --formats srt txt json
            python -m whisper_transcriber --task translate
            python -m whisper_transcriber --verbose
            """,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        "--model",
        type=str,
        default="base",
        help=(
            "Whisper model to use "
            "(tiny, base, small, medium, large-v3, large-v3-turbo)"
        )
    )

    parser.add_argument(
        "--device",
        type=str,
        default="cuda",
        choices=["cpu", "cuda"],
        help="Inference device"
    )

    parser.add_argument(
        "--compute_type",
        type=str,
        default="float16",
        choices=["float32", "float16", "int8"],
        help="Precision / quantization mode"
    )

    parser.add_argument(
        "--language",
        type=str,
        default=None,
        help="Language code (es, en, fr...). Auto-detect if omitted"
    )

    parser.add_argument(
        "--task",
        type=str,
        default="transcribe",
        choices=["transcribe", "translate"],
        help="Transcribe original audio or translate to English"
    )

    parser.add_argument(
        "--input",
        type=str,
        default="data/input",
        help="Input directory"
    )

    parser.add_argument(
        "--output",
        type=str,
        default="data/output",
        help="Output directory"
    )

    parser.add_argument(
        "--formats",
        type=str,
        nargs="+",
        choices=["txt", "srt", "vtt", "json", "tsv"],
        default=["txt", "srt"],
        help="Output formats"
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show live transcription progress"
    )

    return parser.parse_args()