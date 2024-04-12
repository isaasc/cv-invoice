import pytesseract
from PIL import Image
import cv2
import argparse
import pandas as pd
import os
import numpy as np

filename = "cupomfiscal2.png"

image = cv2.imread("./testes/" + filename)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

kernel = np.ones((2, 2), np.uint8)
# gray = cv2.erode(gray, kernel, iterations=2)
# gray = cv2.dilate(gray, kernel, iterations=1) # esses dois juntos funciona melhor pro cupomfiscal.jpg


gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]  # funciona melhor pro cupomfiscal2.png
# gray = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=1)
# elif args["preprocess"] == "blur":
# gray = cv2.medianBlur(gray, 1)

cv2.imwrite(filename, gray)
text = pytesseract.image_to_string(Image.open(filename))
os.remove(filename)
print(text)

cv2.imshow("Image", image)
cv2.imshow("Output", gray)
cv2.waitKey(0)
