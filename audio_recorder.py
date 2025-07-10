import threading
import os
import sys
import wave
import time
from datetime import datetime
import audioop

try:
    import keyboard
    import pyaudio
except ImportError:
    print("Required packages not found. Please install 'keyboard' and 'pyaudio'.")
    sys.exit(1)

date_dir = datetime.now().strftime('%Y%m%d')
AUDIO_DIR = os.path.join(os.path.dirname(__file__), f'audios/{date_dir}')
if not os.path.exists(AUDIO_DIR):
    os.makedirs(AUDIO_DIR)
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
MAX_RECORD_SECONDS = 300  # 5 minutes
SILENCE_SECONDS = 5
SILENCE_THRESHOLD = 500  # Adjust as needed for your mic/environment

class AudioRecorder:
    def __init__(self):
        self.recording = False
        self.audio_thread = None
        self.paused = False
        self.p = pyaudio.PyAudio()

    def _get_new_filename(self):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        return os.path.join(AUDIO_DIR, f"recording_{timestamp}.wav")

    def _record_audio(self):
        stream = self.p.open(format=FORMAT,
                             channels=CHANNELS,
                             rate=RATE,
                             input=True,
                             frames_per_buffer=CHUNK)
        print("Recording... (press Ctrl+Shift+S again to stop)")
        frames = []
        start_time = time.time()
        last_sound_time = time.time()
        file_start_time = time.time()
        filename = self._get_new_filename()
        wf = wave.open(filename, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(self.p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        print(f"Recording to {filename}")

        while self.recording:
            data = stream.read(CHUNK, exception_on_overflow=False)
            rms = audioop.rms(data, 2)  # 2 bytes per sample
            now = time.time()

            if rms > SILENCE_THRESHOLD:
                frames.append(data)
                last_sound_time = now
                if self.paused:
                    print("Speech detected, resuming recording.")
                    self.paused = False
                    # Start a new file after pause
                    filename = self._get_new_filename()
                    wf = wave.open(filename, 'wb')
                    wf.setnchannels(CHANNELS)
                    wf.setsampwidth(self.p.get_sample_size(FORMAT))
                    wf.setframerate(RATE)
                    print(f"Recording to {filename}")
            else:
                if not self.paused and now - last_sound_time > SILENCE_SECONDS:
                    print("Silence detected, pausing recording.")
                    self.paused = True
                    # Save current file
                    if frames:
                        wf.writeframes(b''.join(frames))
                        wf.close()
                        print(f"Audio saved to {filename}")
                        frames = []
                    continue
                if not self.paused:
                    frames.append(data)

            # Check for 10 minute split
            if now - file_start_time >= MAX_RECORD_SECONDS:
                if frames:
                    wf.writeframes(b''.join(frames))
                    wf.close()
                    print(f"Audio saved to {filename}")
                    frames = []
                filename = self._get_new_filename()
                wf = wave.open(filename, 'wb')
                wf.setnchannels(CHANNELS)
                wf.setsampwidth(self.p.get_sample_size(FORMAT))
                wf.setframerate(RATE)
                print(f"Recording to {filename}")
                file_start_time = now

        # On stop, save any remaining audio
        if frames and not self.paused:
            wf.writeframes(b''.join(frames))
            wf.close()
            print(f"Audio saved to {filename}")
        stream.stop_stream()
        stream.close()

    def start_recording(self):
        if self.recording:
            print("Already recording.")
            return
        self.recording = True
        self.audio_thread = threading.Thread(target=self._record_audio, daemon=True)
        self.audio_thread.start()

    def stop_recording(self):
        if not self.recording:
            print("Not currently recording.")
            return
        self.recording = False
        if self.audio_thread:
            self.audio_thread.join()
        print("Stopped recording.")

    def run(self):
        print("Press Ctrl+Shift+S to start/stop recording. Press ESC to exit.")
        keyboard.add_hotkey('ctrl+shift+s', self._toggle_recording)
        keyboard.wait('esc')
        if self.recording:
            self.stop_recording()
        print("Exiting...")

    def _toggle_recording(self):
        if self.recording:
            self.stop_recording()
        else:
            self.start_recording()

if __name__ == '__main__':
    recorder = AudioRecorder()
    recorder.run() 