import cv2
import numpy as np

# large = cv2.imread('sample_text.png')
# rgb = cv2.pyrDown(large)
# small = cv2.cvtColor(rgb, cv2.COLOR_BGR2GRAY)

# # kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
# kernel = np.ones((5, 5), np.uint8)
# grad = cv2.morphologyEx(small, cv2.MORPH_GRADIENT, kernel)

# _, bw = cv2.threshold(grad, 0.0, 255.0, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

# kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 1))
# connected = cv2.morphologyEx(bw, cv2.MORPH_CLOSE, kernel)

# # using RETR_EXTERNAL instead of RETR_CCOMP
# contours, hierarchy = cv2.findContours(connected.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# #For opencv 3+ comment the previous line and uncomment the following line
# #_, contours, hierarchy = cv2.findContours(connected.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

# mask = np.zeros(bw.shape, dtype=np.uint8)

# for idx in range(len(contours)):
#     x, y, w, h = cv2.boundingRect(contours[idx])
#     mask[y:y+h, x:x+w] = 0
#     cv2.drawContours(mask, contours, idx, (255, 255, 255), -1)
#     r = float(cv2.countNonZero(mask[y:y+h, x:x+w])) / (w * h)

#     if r > 0.45 and w > 8 and h > 8:
#         cv2.rectangle(rgb, (x, y), (x+w-1, y+h-1), (0, 255, 0), 2)


# cv2.imshow('rects', rgb)
# cv2.waitKey(0)

# Load image, grayscale, Gaussian blur, Otsu's threshold
image = cv2.imread('sample_text.png')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (7,7), 0)
thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

# Create rectangular structuring element and dilate
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
dilate = cv2.dilate(thresh, kernel, iterations=4)

# Find contours and draw rectangle
cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
for c in cnts:
    x,y,w,h = cv2.boundingRect(c)
    cv2.rectangle(image, (x, y), (x + w, y + h), (36,255,12), 2)

cv2.imshow('thresh', thresh)
cv2.imshow('dilate', dilate)
cv2.imshow('image', image)
cv2.waitKey()