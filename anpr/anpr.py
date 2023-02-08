import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd='C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

# Load the image

img = cv2.imread("img_1.png")

# Convert the image to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Apply Gaussian Blur to remove noise
blur = cv2.GaussianBlur(gray, (5,5), 0)

# Apply Adaptive Threshold to enhance the image
thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

# Find contours in the image
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Iterate through the contours and select the contour with the largest area
largest_contour = None
largest_area = 0
for contour in contours:
    area = cv2.contourArea(contour)
    if area > largest_area:
        largest_area = area
        largest_contour = contour

# Draw a rectangle around the largest contour to get the number plate
if largest_contour is not None:
    x, y, w, h = cv2.boundingRect(largest_contour)
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    number_plate = img[y:y+h, x:x+w]

# Use OCR (Optical Character Recognition) to extract the number from the number plate
text = pytesseract.image_to_string(number_plate, lang="eng")

# Print the extracted number
print("Extracted number:", text)
