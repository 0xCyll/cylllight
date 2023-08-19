# cylllight
An easier way to use nightlight(dbd) with one click of a python script!
## how do i use this?
Either build the program yourself using pyinstaller and having the libraries installed or download the latest build from releases tab. Make sure to grab an api key from https://nightlight.gg/account/api and press "Configure API key" in the program to paste your api key inside :D .
# Monitoring whas it that?
The enable monitoring option allows the program to automatically detect when your game is done and when you are on the score tab for around 3 seconds it will take a screenshot and upload it for you.

# how do i build?
download the dependencies and run ```python -m PyInstaller --add-data "C:\Program Files\Tesseract-OCR;tesseract" --add-data "success.wav;." --onedir -w main.py```
## Antivirus flagged?
due to how i built this using pyinstaller it causes a few antivirus software to list it as a false positive, I will try working around this
