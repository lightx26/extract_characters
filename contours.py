import os
import hashlib
import random
import string
import time

import cv2
# import pytesseract


def preprocess_image(img, ksize):
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh_image = cv2.threshold(255 - gray_image, 127, 255, cv2.THRESH_BINARY)
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, ksize)

    # Applying dilation on the threshold image
    dilation = cv2.dilate(thresh_image, rect_kernel, iterations=1)
    return dilation


def resize_image(img, scale_percent=60, new_size=(600, 400)):
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    return cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)


def find_contours(thresh_image):
    contours, hierarchy = cv2.findContours(thresh_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    return contours


def filter_contours(contours):
    _contours = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        # Filter based on aspect ratio, area, and other desired criteria
        if area > 150:
            _contours.append(cnt)

    return _contours


# def draw_contours(image, contours):
#     cv2.drawContours(image, contours, -1, (0, 255, 0), 1)
#     cv2.imshow("Contours", image)


def draw_rectangles(image, rectangles, title):
    for rec in rectangles:
        x, y, w, h = rec
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 1)
    # cv2.imshow(title, image)


def detect_text_regions(image, contours):
    text_regions = []
    for i, contour in enumerate(contours):
        x, y, w, h = cv2.boundingRect(contour)
        text_regions.append(image[y:y + h, x:x + w])
    return text_regions


def detect_word(image_path, ksize):
    img = cv2.imread(image_path)
    resized_image = resize_image(img)

    # Preprocessing
    processed_image = preprocess_image(resized_image, (25, 30))

    # Find text contours
    contours = find_contours(processed_image)
    filtered_contours = filter_contours(contours)

    # Find text regions
    text_regions = detect_text_regions(resized_image, filtered_contours)

    words = []
    for i, region in enumerate(text_regions):
        tmp_thresh_image = preprocess_image(region, ksize)
        tmp_thresh_image = find_contours(tmp_thresh_image)
        tmp_filtered_contours = filter_contours(tmp_thresh_image)

        region2 = region.copy()
        for cnt in tmp_filtered_contours:
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(region2, (x, y), (x + w, y + h), (0, 255, 0), 1)
            words.append(region[y:y + h, x:x + w])
        # cv2.imshow(f"Word {i}", region2)
    return words


# def detect_character(text_regions):
#     words = []
#     print(len(text_regions))
#     for i, region in enumerate(text_regions):
#         tmp_thresh_image = preprocess_image(region, (ã, g))
#         tmp_thresh_image = find_contours(tmp_thresh_image)
#         tmp_filtered_contours = filter_contours(tmp_thresh_image)
#
#         for i, cnt in enumerate(tmp_filtered_contours):
#             x, y, w, h = cv2.boundingRect(cnt)
#             cv2.rectangle(region, (x, y), (x + w, y + h), (0, 255, 0), 1)
#         # draw_rectangles(region, tmp_filtered_contours)
#         cv2.imshow(f"Word {i}", region)
#     return words


# def extract_words(image):
#     # Preprocessing
#     processed_image = preprocess_image(image, (25, 30))
#
#     # Find text contours
#     contours = find_contours(processed_image)
#     filtered_contours = filter_contours(contours)
#
#     text_regions = detect_text_regions(image, filtered_contours)
#     detect_word(text_regions)


def extract_characters(words, ksize, output_folder='output_character'):
    for word in words:
        prep = preprocess_image(word, ksize)
        contours = find_contours(prep)
        filtered_contours = filter_contours(contours)

        for cnt in filtered_contours:
            x, y, w, h = cv2.boundingRect(cnt)
            character = word[y:y + h, x:x + w]

            # text = pytesseract.image_to_string(character, config='--psm 10').strip()
            # print(text)

            # # Create the folder if it doesn't exist
            # os.makedirs(os.path.join(output_folder, text), exist_ok=True)

            # Create a unique filename using timestamp
            timestamp = int(time.time())
            random_string = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(5))

            filename = f"{timestamp}_{random_string}.png"

            # filepath = os.path.join(output_folder, text, filename)
            filepath = os.path.join(output_folder, filename)

            # Write the character image to the file
            cv2.imwrite(filepath, character)


image_path = 'input_image/1.jpg'

# Configure the kernel size for word detection
detected_words = detect_word(image_path, (10, 8))

# Configure the kernel size for character extraction
extract_characters(detected_words, ksize=(1, 5))

cv2.waitKey(0)
cv2.destroyAllWindows()
