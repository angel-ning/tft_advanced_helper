import os
import time
import pyscreenshot as ImageGrab
import pytesseract
from PIL import Image
import keyboard

# Define the coordinates for the champion boxes in the shop
champ_box = [
    (480, 930, 670, 1070),
    (680, 930, 870, 1070),
    (880, 930, 1070, 1070),
    (1080, 930, 1270, 1070),
    (1290, 930, 1480, 1070),
]

# Get the current directory of the script
current_directory = os.getcwd()
# Create the 'champion_cards' directory if it doesn't exist
cards_directory = os.path.join(current_directory, 'champion_cards')
os.makedirs(cards_directory, exist_ok=True)

# Path for the log file
log_path = os.path.join(current_directory, 'champ_names_log.txt')
# Open the file in append mode
log_file = open(log_path, 'a', encoding='utf8')

def capture_and_log_champs():
    # Iterate over the champion boxes
    for index, box in enumerate(champ_box):
        # Capture the image of the champion box
        champ_img = ImageGrab.grab(bbox=box)
        # Save the screenshot in the 'champion_cards' directory
        # screenshot_filename = f'champ_box_{index}_{int(time.time())}.png'
        # screenshot_path = os.path.join(cards_directory, screenshot_filename)
        # champ_img.save(screenshot_path)
        # # Use pytesseract to read the champion name
        champ_name = pytesseract.image_to_string(champ_img, lang='eng').strip()
        # Print and log the recognized name
        output_string = f'Champion Box {index + 1}: {champ_name}\n'
        print(output_string, end='')
        log_file.write(output_string)
    # Flush the output to the file
    log_file.flush()

def main():
    print("Press 'k' to capture champion images and read names.")
    while True:
        try:
            # Wait for 'k' to be pressed
            if keyboard.is_pressed('k'):
                capture_and_log_champs()
                # Add a small delay to prevent multiple captures from a single press
                time.sleep(0.5)
        except KeyboardInterrupt:
            # Exit the loop when a keyboard interrupt is detected (Ctrl+C)
            break
    # Close the file when done
    log_file.close()

if __name__ == '__main__':
    main()
