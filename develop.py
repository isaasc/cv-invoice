import pytesseract
from PIL import Image
import cv2
import os
import re
import easyocr
import urllib.request


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


def get_valor_total(text):
    ptr = 'R. *(\\d+,\\d{2})'
    reMatch = re.search(ptr, str(text))

    if reMatch:
        return reMatch.group(1)


def get_CNPJ(text):
    ptr = '\\d{2}\\D\\d{3}\\D\\d{3}\\D\\d{4}\\D\\d{2}'
    reMatch = re.search(ptr, str(text))

    if reMatch:
        return reMatch.group(0)


def get_from_CNPJ(cnpj):
    cnpj = re.sub("\\D", "", cnpj)
    print(cnpj)
    contents = urllib.request.urlopen("https://api-publica.speedio.com.br/buscarcnpj?cnpj=" + cnpj).read()
    return contents


def run_tesseract(filename):
    prepare_image(filename)
    text = pytesseract_process(filename)

    os.remove(filename)

    print(get_valor_total(text))
    cnpj = get_CNPJ(text)
    print(cnpj)
    print(get_from_CNPJ(cnpj))

    # print(text)

