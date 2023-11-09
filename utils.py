# This file contains utility functions like image capture, OCR, etc.
import pyscreenshot as ImageGrab
import pytesseract
import time
from PIL import Image
import pyautogui as pg

def capture_screen(bbox):
    # Capture and return the image from the screen
    return ImageGrab.grab(bbox=bbox)

def read_text_from_image(image):
    return pytesseract.image_to_string(image, lang='eng').strip()

def read_digit_from_image(image):
    config = r'--oem 3 --psm 6 outputbase digits'
    return pytesseract.image_to_string(image, config=config)

def left_slow_click(p, button='PRIMARY', move_time=0.2, down_time=0.2, up_time=0.2):
    pg.click(p[0], p[1], duration=move_time)
    pg.mouseDown(p[0], p[1], button=button, duration=down_time)
    pg.mouseUp(p[0], p[1], button=button, duration=up_time)

    return True

def if_check_word(x1, y1, x2, y2, target):

    title = read_text_from_image(capture_screen(bbox=(x1, y1, x2, y2)))

    if target in title:
        return True
    else:
        return False
    
def slow_key_press(key, down_time=0.2):
    pg.press(key)  # Using pyautogui to press the key
    time.sleep(down_time)

def get_box_center(box):
    x = int((box[2] - box[0]) / 2) + box[0]
    y = int((box[3] - box[1]) / 2) + box[1]

    return (x, y)