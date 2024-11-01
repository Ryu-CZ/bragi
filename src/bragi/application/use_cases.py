# application/use_cases.py
import signal
import sys
from ..domain.services import DenoiseChunk
from ..infrastructure.audio_io import AudioIO
from ..infrastructure.device_manager import VirtualMicrophone
from ..infrastructure.noise_reduction import apply_noise_reduction


def start_noise_cancellation(denoise_fn: DenoiseChunk| None = None):
    if denoise_fn is None:
        denoise_fn = apply_noise_reduction
    virtual_mic = VirtualMicrophone("bragi_microphone")
    sink_name = virtual_mic.sink_name

    # Initialize Audio IO
    audio_io = AudioIO(output_device_index=find_device_index(sink_name))

    def signal_handler(sig, frame):
        print("Interrupt received, shutting down...")
        audio_io.close()
        virtual_mic.unload_virtual_mic()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    try:
        while True:
            audio_chunk = audio_io.read_audio_chunk()
            processed_chunk = denoise_fn(audio_chunk)
            audio_io.write_audio_chunk(processed_chunk)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        audio_io.close()
        virtual_mic.unload_virtual_mic()


def find_device_index(device_name):
    import pyaudio

    p = pyaudio.PyAudio()
    device_index = None
    for i in range(p.get_device_count()):
        dev = p.get_device_info_by_index(i)
        if device_name in dev["name"]:
            device_index = i
            break
    p.terminate()
    if device_index is None:
        print(f"Device '{device_name}' not found.")
    return device_index
