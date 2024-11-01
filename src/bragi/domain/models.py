# domain/models.py

from dataclasses import dataclass
import numpy as np


@dataclass
class AudioChunk:
    data: np.ndarray
    sample_rate: int
