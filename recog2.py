import cv2
import numpy as np

# Read the image
image = cv2.imread('test7.png', cv2.IMREAD_GRAYSCALE)

# Apply image processing (e.g., thresholding)
_, binary_image = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY_INV)

# Find contours
contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Extract individual letters based on contours and print/display them
for contour in contours:
    x, y, w, h = cv2.boundingRect(contour)
    letter = image[y:y+h, x:x+w]

    # Display the extracted letter
    cv2.imshow('Extracted Letter', letter)
    cv2.waitKey(0)  # Wait for a key press to proceed to the next letter

cv2.destroyAllWindows()  # Close the window when done
