# KeepNotes

KeepNotes is a two-part application for capturing and organizing voice notes. It allows you to record your voice, automatically saves the audio as `.wav` files, and transcribes them into text. You can further organize your transcriptions into groups using an AI tool and a simple configuration file.

## Features

- **Voice Recording:**
  - Record your voice using a hotkey.
  - Audio is saved as `.wav` files, organized by date in the `audios/` folder.
- **Automatic Transcription:**
  - Every 30 seconds, the application checks for new audio files and transcribes them into text using Google Speech Recognition.
  - Transcriptions are appended to `transcriptions.txt`.
- **AI-Powered Organization:**
  - Use the `analyse-transcriptions` file to define groups for your notes.
  - With the help of an AI tool (like ChatGPT or Claude), you can split `transcriptions.txt` into group-based files in the `groups/` folder.

## Folder Structure

```
KeepNotes/
├── audios/
│   └── YYYYMMDD/           # Daily folders for .wav audio files
├── groups/                 # Output folder for group-based text files
├── transcriptions.txt      # All transcribed text notes
├── audio_recorder.py       # Voice recording script
├── audio_to_text.py        # Transcription script
├── analyse-transcriptions  # Group configuration for AI tools
├── requirements.txt        # Python dependencies
├── run_audio_tools.bat     # Windows batch script to run both apps
```

## Getting Started

### 1. Install Dependencies

Make sure you have Python 3.x installed. Then, install the required packages:

```bash
pip install -r requirements.txt
```

### 2. Start the Applications

On Windows, you can use the provided batch script:

```bash
run_audio_tools.bat
```

This will open two terminals:
- One for recording audio (`audio_recorder.py`)
- One for transcribing audio (`audio_to_text.py`)

#### Manual Start

Alternatively, you can run the scripts manually:

```bash
python audio_recorder.py
python audio_to_text.py
```

### 3. Record Voice Notes

- Press `Ctrl+Shift+S` to start/stop recording.
- Press `ESC` to exit the recorder.
- Audio files are saved in `audios/YYYYMMDD/`.

### 4. Transcription

- The transcriber checks for new `.wav` files every 30 seconds and appends recognized text to `transcriptions.txt`.

### 5. Organize Notes with AI

- Edit the `analyse-transcriptions` file to define your groups (e.g., `BDSR`, `MyWorkManagement`, `STU`, `WTU`).
- Use an AI tool (like ChatGPT or Claude) to process `transcriptions.txt` according to the instructions in `analyse-transcriptions`.
- The AI will split the notes into group files (e.g., `group_BDSR_YYYYMMDD.txt`) in the `groups/` folder.

## Example `analyse-transcriptions` File

```
I WANT YOU TO DO THESE TASKS (DO NOT SHOW ME WHAT YOU ARE DOING):

    Improve the text in @transcriptions.txt

    Classify the notes in @transcriptions.txt based on these groups: 
    - BDSR
    - MyWorkManagement
    - STU
    - WTU
    PAY ATTENTION THAT COULD BE MORE SEPARATE SECTIONS IN @transcriptions.txt FOR THE SAME GROUP
    LEAVE @transcriptions.txt AS IT IS.

    After the classification:
    CREATE A NEW FILE for each group and copy the relative sections in them.
    The file name has to have this pattern group_YYYYMMDD 
    and have to be create in the folder KeepNotes/groups
```

## Notes
- The `audios/` and `groups/` folders are ignored by git (see `.gitignore`).
- The application is designed for Windows, but the Python scripts can be adapted for other OSes.
- You need an internet connection for Google Speech Recognition.

## License

MIT License (or specify your license here) 