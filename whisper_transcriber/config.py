from dataclasses import dataclass


@dataclass
class Config:
    model: str
    device: str
    compute_type: str
    input_dir: str
    output_dir: str