# domain/services.py
import typing
from .models import AudioChunk

class DenoiseChunk(typing.Protocol):
    """
    Function for applying noise reduction.
    """

    def __call__(self, audio_chunk: AudioChunk) -> AudioChunk:
        """
        Args:
            audio_chunk (AudioChunk): The audio chunk to process.

        Returns:
            AudioChunk: The processed audio chunk.
        """
        pass


