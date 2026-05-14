from whisper_transcriber.cli import parse_args
from whisper_transcriber.config import Config
from whisper_transcriber.transcriber import (
    create_model,
    process_input_files
)
from whisper_transcriber.logger import setup_logger

logger = setup_logger()

def main():
    args = parse_args()

    config = Config(
        model=args.model,
        device=args.device,
        compute_type=args.compute_type,
        language=args.language,
        task=args.task,
        input_dir=args.input,
        output_dir=args.output,
    )

    model = create_model(config)

    process_input_files(model, config)


if __name__ == "__main__":
    main()