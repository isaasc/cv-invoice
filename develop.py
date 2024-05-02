import pytesseract
from PIL import Image
import cv2
import os
import re
import easyocr


def prepare_image(filename):
    image = cv2.imread("./tests/" + filename)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]  # funciona melhor pro cupomfiscal2.png
    cv2.imwrite(filename, gray)
#   kernel = np.ones((2, 2), np.uint8)
#   gray = cv2.erode(gray, kernel, iterations=2)
#   gray = cv2.dilate(gray, kernel, iterations=1)
#   gray = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=1)
#   elif args["preprocess"] == "blur":
#   gray = cv2.medianBlur(gray, 1)


def pytesseract_process(filename):
    text = pytesseract.image_to_string(Image.open(filename), config='--psm 4')
    return text


def easyocr_process(filename):
    reader = easyocr.Reader(['en'], model_storage_directory='./EasyOCR/model/english_g2.pth')
    result = reader.readtext(filename)
    return result


def evaluate_success(text):
    ptr = 'R(?:S|\\$) +(\\d+,\\d{2})'
    reMatch = re.search(ptr, str(text))

    if reMatch:
        result = reMatch.group(1)
        # print("sucesso: " + result)
        return result
    else:
        return None


def run_tesseract(filename):
    prepare_image(filename)
    text = pytesseract_process(filename)
    # text = easyocr_process(filename)
    result = evaluate_success(text)

    os.remove(filename)

    print(text)
    # print(f"EasyOCR\n\tTest: {filename}\n\t\tResult: {result}\n")


def run_easyocr(filename):
    prepare_image(filename)
    # text = pytesseract_process(filename)
    text = easyocr_process(filename)
    result = evaluate_success(text)

    os.remove(filename)

    print(text)
    # print(f"EasyOCR\n\tTest: {filename}\n\t\tResult: {result}\n")

# cv2.imshow("Image", image)
# cv2.imshow("Output", gray)
# cv2.waitKey(0)
