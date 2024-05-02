import matplotlib.pyplot as plt
import cv2
import numpy as np

image = cv2.imread("./tests/cupomfiscal3.jpg")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# ret, thresh = cv2.threshold(gray, 127, 255, 0)
# im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# bf = cv2.BFMatcher()
# # cv2.drawContours(image, [contours], 0, (0, 255, 0), 3)
# sift = cv2.SIFT.create(nfeatures=5000)
# kp, desc = sift.detectAndCompute(gray, None)
# matches = bf.knnMatch()

#
# img = cv2.drawKeypoints(gray, kp, image)
# cv2.imwrite('sift_keypoints.jpg', img)

cA, cB, cC, cD = [87, 354], [1446, 380], [61, 2934], [1429, 2952]

width_AD = np.sqrt(((cA[0] - cD[0]) ** 2) + ((cA[1] - cD[1]) ** 2))
width_BC = np.sqrt(((cB[0] - cC[0]) ** 2) + ((cB[1] - cC[1]) ** 2))
maxWidth = max(int(width_AD), int(width_BC))

height_AB = np.sqrt(((cA[0] - cB[0]) ** 2) + ((cA[1] - cB[1]) ** 2))
height_CD = np.sqrt(((cC[0] - cD[0]) ** 2) + ((cC[1] - cD[1]) ** 2))
maxHeight = max(int(height_AB), int(height_CD))

input_pts = np.float32([cA, cB, cC, cD])
output_pts = np.float32([[0, 0],
                        [0, maxHeight - 1],
                        [maxWidth - 1, maxHeight - 1],
                        [maxWidth - 1, 0]])

M = cv2.getPerspectiveTransform(input_pts, output_pts)

out = cv2.warpPerspective(image , M, (maxWidth, maxHeight), flags=cv2.INTER_LINEAR)

plt.imshow(out, cmap='gray')
plt.title(f'Cupom')
plt.show()
