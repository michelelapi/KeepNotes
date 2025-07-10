import os
import sys
import time
from datetime import datetime

try:
    import speech_recognition as sr
except ImportError:
    print("Required packages not found. Please install 'speechrecognition'.")
    sys.exit(1)

TRANSCRIPTIONS_FILE = os.path.join(os.path.dirname(__file__), 'transcriptions.txt')
date_dir = datetime.now().strftime('%Y%m%d')
AUDIO_DIR = os.path.join(os.path.dirname(__file__), f'audios/{date_dir}')
CHECK_INTERVAL = 30  # seconds
STABLE_TIME = 3     # seconds to check if file size is stable

class AudioToText:
    def __init__(self, audio_dir=AUDIO_DIR, transcriptions_file=TRANSCRIPTIONS_FILE):
        self.audio_dir = audio_dir
        self.transcriptions_file = transcriptions_file
        self.recognizer = sr.Recognizer()
        self.transcribed_files = set()
        self._load_transcribed_files()

    def _load_transcribed_files(self):
        if not os.path.exists(self.transcriptions_file):
            return
        with open(self.transcriptions_file, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) > 1 and parts[1].startswith('recording_'):
                    self.transcribed_files.add(parts[1])

    def _is_file_stable(self, filepath):
        size1 = os.path.getsize(filepath)
        time.sleep(STABLE_TIME)
        size2 = os.path.getsize(filepath)
        return size1 == size2

    def transcribe_existing(self):
        """Transcribe all existing .wav files that have not been transcribed yet, regardless of age."""
        wav_files = [f for f in os.listdir(self.audio_dir) if f.lower().endswith('.wav')]
        for wav_file in wav_files:
            if wav_file in self.transcribed_files:
                continue
            audio_path = os.path.join(self.audio_dir, wav_file)
            # Check if file is stable (not being written to)
            try:
                if not self._is_file_stable(audio_path):
                    continue
            except Exception as e:
                print(f"Error checking file {wav_file}: {e}")
                continue
            # Get file modification time
            mod_time = os.path.getmtime(audio_path)
            dt_str = datetime.fromtimestamp(mod_time).strftime('%Y-%m-%d %H:%M:%S')
            print(f"Transcribing {wav_file} (initial pass)...")
            try:
                with sr.AudioFile(audio_path) as source:
                    audio = self.recognizer.record(source)
                text = self.recognizer.recognize_google(audio)
                self._save_transcription(dt_str, wav_file, text)
                print(f"{wav_file}: {text}")
                self.transcribed_files.add(wav_file)
            except sr.UnknownValueError:
                print(f"{wav_file}: Could not understand audio.")
                self.transcribed_files.add(wav_file)
            except Exception as e:
                print(f"{wav_file}: Transcription error: {type(e).__name__}: {e}")

    def transcribe_all(self):
        # First, transcribe all existing files (regardless of age)
        self.transcribe_existing()
        print(f"Monitoring {self.audio_dir} for new audio files...")
        while True:
            wav_files = [f for f in os.listdir(self.audio_dir) if f.lower().endswith('.wav')]
            for wav_file in wav_files:
                if wav_file in self.transcribed_files:
                    continue
                audio_path = os.path.join(self.audio_dir, wav_file)
                # Check if file is stable (not being written to)
                try:
                    if not self._is_file_stable(audio_path):
                        continue
                except Exception as e:
                    print(f"Error checking file {wav_file}: {e}")
                    continue
                # Check if file is older than 10 minutes
                file_age_seconds = time.time() - os.path.getmtime(audio_path)
                if file_age_seconds < 600:  # 600 seconds = 10 minutes
                    continue
                # Get file modification time
                mod_time = os.path.getmtime(audio_path)
                dt_str = datetime.fromtimestamp(mod_time).strftime('%Y-%m-%d %H:%M:%S')
                print(f"Transcribing {wav_file}...")
                try:
                    with sr.AudioFile(audio_path) as source:
                        audio = self.recognizer.record(source)
                    text = self.recognizer.recognize_google(audio)
                    self._save_transcription(dt_str, wav_file, text)
                    print(f"{wav_file}: {text}")
                    self.transcribed_files.add(wav_file)
                except sr.UnknownValueError:
                    print(f"{wav_file}: Could not understand audio.")
                    self.transcribed_files.add(wav_file)
                except Exception as e:
                    print(f"{wav_file}: Transcription error: {type(e).__name__}: {e}")
            time.sleep(CHECK_INTERVAL)

    def _save_transcription(self, dt_str, filename, text):
        with open(self.transcriptions_file, 'a', encoding='utf-8') as f:
            f.write(f"{dt_str}: {text}\n")

if __name__ == '__main__':
    at = AudioToText()
    at.transcribe_all() 