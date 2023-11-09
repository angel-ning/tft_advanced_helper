# TFT helper

## Description

This project is designed to automate certain actions within a game environment. It utilizes image recognition through Google Tesseract OCR to read text from the game screen and perform actions based on predefined conditions. The script can start and stop gameplay, find matches, accept matches, and more based on in-game stages or events.

## Environment Setup

### Requirements:

- Python 3.6 or higher
- Pillow (PIL Fork)
- Google Tesseract OCR
- Supported systems: Windows / macOS / Linux

This project has been developed and tested on Windows 10.

### Installation

#### 1. Install Google Tesseract OCR

- **Tesseract OCR GitHub repository:** [https://github.com/tesseract-ocr/tesseract](https://github.com/tesseract-ocr/tesseract)
- **Windows Tesseract download link:** [https://digi.bib.uni-mannheim.de/tesseract/](https://digi.bib.uni-mannheim.de/tesseract/)
- **macOS and Linux installation guide:** [Tesseract OCR Installation](https://tesseract-ocr.github.io/tessdoc/Installation.html)

#### 2. Install Required Python Packages

Install the required Python packages using `pip`:

```bash
pip install pillow pytesseract pyautogui keyboard
```

Note: Depending on your system, you might need to use pip3 instead of pip.

### Usage

To use this script, simply run the `main.py` file from your terminal:

```bash
python main.py
```
Or on some systems:
```bash
python3 main.py
```
### Controls
- Press q to stop the automation script.
- Hotkeys and other controls are defined within the script and can be customized as needed.

### Features
- Text recognition from the game screen.
- Game start, stop, and find match automation.
- In-game action automation based on stage detection.
- Logging system to track actions and events.

### Contributing
- Contributions to this project are welcome. Please ensure that you update tests as appropriate.

### License

[MIT](https://choosealicense.com/licenses/mit/)

### Disclaimer
This project is for educational purposes only. The author is not responsible for any misuse or damage caused by this program.
