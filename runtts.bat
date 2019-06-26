@echo off
set /p intext="input text: "
py -3 ttsfbfe/tts.py "%intext%"
echo Output is in output.wav
pause