from gtts import gTTS
import os
from PIL import Image
import pytesseract

# Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def image_to_text(image_path):
    # Open the image using Pillow (PIL)
    img = Image.open(image_path)

    # Perform OCR on the image
    text = pytesseract.image_to_string(img)

    return text


def text_to_speech(text, language='en-au', file_name='output.mp3'):
    # Create a gTTS object
    tts = gTTS(text=text, lang=language, slow=False)

    # Save the converted speech to a file
    tts.save(file_name)

    # Play the generated speech using the default audio player
    os.system(f'start {file_name}')


# Extract text from image
image_path = 'input_image/walloftext.jpg'
result_text = image_to_text(image_path)
print(result_text)

# Push data (text, audio, image) to the cloud

# Convert text to speech
text_to_speech(result_text)