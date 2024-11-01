# infrastructure/noise_reduction.py

import librosa
import tensorflow as tf
import numpy as np
from bragi.domain.models import AudioChunk
from bragi.domain.services import apply_noise_reduction as domain_apply_noise_reduction


class NoiseReducer:
    def __init__(self, model_path=None):
        # Load your trained noise reduction model
        if model_path:
            self.model = tf.keras.models.load_model(model_path)
        else:
            # Placeholder: define or load a model
            self.model = self._build_dummy_model()

    def _build_dummy_model(self):
        # Simple example model for illustration
        input_shape = (None, 1)
        model = tf.keras.Sequential(
            [
                tf.keras.layers.InputLayer(input_shape=input_shape),
                tf.keras.layers.Dense(64, activation="relu"),
                tf.keras.layers.Dense(1),
            ]
        )
        return model

    def reduce_noise(self, audio_chunk):
        # Preprocess audio data
        y = audio_chunk.data
        sr = audio_chunk.sample_rate

        # Example: Use spectrograms for processing
        S = librosa.stft(y, n_fft=512, hop_length=256)
        S_magnitude, S_phase = np.abs(S), np.angle(S)

        # Prepare input for the model
        S_magnitude = np.expand_dims(
            S_magnitude.T, axis=-1
        )  # Shape: (frames, freq_bins, 1)

        # Predict
        denoised_magnitude = self.model.predict(S_magnitude)

        # Reconstruct spectrogram
        denoised_magnitude = denoised_magnitude.squeeze().T
        S_denoised = denoised_magnitude * np.exp(1j * S_phase)

        # Inverse STFT to get time-domain signal
        y_denoised = librosa.istft(S_denoised, hop_length=256)

        return AudioChunk(data=y_denoised, sample_rate=sr)


# Override the domain function with the infrastructure implementation
def apply_noise_reduction(audio_chunk):
    noise_reducer = NoiseReducer()
    return noise_reducer.reduce_noise(audio_chunk)
