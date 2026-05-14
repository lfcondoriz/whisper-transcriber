from dataclasses import dataclass


@dataclass
class Config:
    model: str
    device: str
    compute_type: str
    language: str | None
    task: str
    input_dir: str
    output_dir: str