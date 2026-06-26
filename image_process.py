import numpy as np
import base64
import cv2
import easyocr

reader = easyocr.Reader(['en'], gpu=False)


def base64_to_image(base64_data):
    img_bytes = base64.b64decode(base64_data)
    img_array = np.frombuffer(img_bytes, dtype=np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    return img


def preprocess(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return thresh


def solve_captcha_image(img):
    result = reader.readtext(img, detail=0)
    return " ".join(result)
