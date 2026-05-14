def format_timestamp(seconds: float) -> str:
    ms = int((seconds - int(seconds)) * 1000)
    s = int(seconds) % 60
    m = (int(seconds) // 60) % 60
    h = int(seconds) // 3600

    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"