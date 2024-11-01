import pyaudio
import wave
import threading
import time

def record_audio(filename, prompt):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16  # 16-bit resolution
    CHANNELS = 1              # Mono audio
    RATE = 44100              # 4.1kHz sampling rate


    p = pyaudio.PyAudio()

    # Open stream
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    frames = []

    print(prompt)
    input("Press Enter to start recording...")
    print("Recording... Press Enter to stop.")

    # Start recording in a separate thread
    stop_recording = threading.Event()

    def record():
        while not stop_recording.is_set():
            data = stream.read(CHUNK, exception_on_overflow=False)
            frames.append(data)

    recording_thread = threading.Thread(target=record)
    recording_thread.start()

    input()  # Wait for user to press Enter
    stop_recording.set()
    recording_thread.join()

    print("Recording stopped.")

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    p.terminate()

    # Save the recording to a WAV file
    wf = wave.open(filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    print(f"Saved recording to {filename}\n")

def main():
    print("Welcome to the Sample Recorder!")

    # Record clean voice sample
    record_audio('voice.wav', "\nPrepare to record a clean sample of your voice.")
    time.sleep(1)  # Brief pause between recordings

    # Record background noise sample
    record_audio('background.wav', "\nPrepare to record a sample of background noise.")
    time.sleep(1)

    print("All recordings completed.")

if __name__ == '__main__':
    main()
