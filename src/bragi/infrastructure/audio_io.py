# infrastructure/audio_io.py

import pyaudio
import numpy as np

from bragi.domain.models import AudioChunk


class AudioIO:
    def __init__(
        self,
        input_device_index=None,
        output_device_index=None,
        rate=16000,
        chunk_size=1024,
    ):
        self.rate = rate
        self.chunk_size = chunk_size
        self.format = pyaudio.paFloat32
        self.channels = 1
        self.p = pyaudio.PyAudio()

        self.stream_in = self.p.open(
            format=self.format,
            channels=self.channels,
            rate=self.rate,
            input=True,
            input_device_index=input_device_index,
            frames_per_buffer=self.chunk_size,
        )

        self.stream_out = self.p.open(
            format=self.format,
            channels=self.channels,
            rate=self.rate,
            output=True,
            output_device_index=output_device_index,
            frames_per_buffer=self.chunk_size,
        )

    def read_audio_chunk(self):
        data = self.stream_in.read(self.chunk_size, exception_on_overflow=False)
        audio_data = np.frombuffer(data, dtype=np.float32)
        return AudioChunk(data=audio_data, sample_rate=self.rate)

    def write_audio_chunk(self, audio_chunk):
        data = audio_chunk.data.astype(np.float32).tobytes()
        self.stream_out.write(data)

    def close(self):
        self.stream_in.stop_stream()
        self.stream_in.close()
        self.stream_out.stop_stream()
        self.stream_out.close()
        self.p.terminate()
