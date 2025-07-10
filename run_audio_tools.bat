@echo off
cd /d %~dp0

REM Run audio_to_text.py in a new terminal window
start "AudioToText" cmd /k python audio_to_text.py

REM Run audio_recorder.py in another new terminal window
start "AudioRecorder" cmd /k python audio_recorder.py

pause 