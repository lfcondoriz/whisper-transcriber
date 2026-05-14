from whisper_transcriber.cli import parse_args
from whisper_transcriber.config import Config
from whisper_transcriber.core.model import create_model
from whisper_transcriber.core.transcriber import process_input_files


def main():
    args = parse_args()

    config = Config(
        model=args.model,
        device=args.device,
        compute_type=args.compute_type,
        input_dir=args.input,
        output_dir=args.output,
        language=args.language,
        task=args.task
    )

    model = create_model(config)

    process_input_files(model, config)


if __name__ == "__main__":
    main()