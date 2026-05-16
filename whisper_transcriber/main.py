from whisper_transcriber.cli import parse_args
from whisper_transcriber.config import Config
from whisper_transcriber.core.transcriber import WhisperTranscriber

def main():
    args = parse_args()

    # 1. Armamos la configuración
    config = Config(
        model=args.model,
        device=args.device,
        compute_type=args.compute_type,
        input_dir=args.input,
        output_dir=args.output,
        language=args.language,
        task=args.task
    )

    # 2. Instanciamos nuestra nueva clase
    transcriber = WhisperTranscriber(config)

    # 3. Ejecutamos el flujo
    transcriber.process_all()

if __name__ == "__main__":
    main()