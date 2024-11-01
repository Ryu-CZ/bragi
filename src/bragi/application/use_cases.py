# application/use_cases.py
import signal
import sys
from bragi.domain.services import apply_noise_reduction
from bragi.infrastructure.audio_io import AudioIO
from bragi.infrastructure.device_manager import VirtualMicrophone

import threading


def start_noise_cancellation():
    virtual_mic = VirtualMicrophone()
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
            processed_chunk = apply_noise_reduction(audio_chunk)
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
