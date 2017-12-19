import numpy as np
import cv2 as cv
import utils

# Load the image
folder = "data/"
image = cv.imread(folder + "table.jpg")

# Resize image
# size = (800, 900) # rows and columns in image
# resized = cv.resize(image, size)
resized = image.copy()

# Convert resized RGB image to grayscale
NUM_CHANNELS = 3
if len(image.shape) == NUM_CHANNELS:
    grayscale = cv.cvtColor(resized, cv.COLOR_BGR2GRAY)

# =====================================================
# Adaptive thresholding
"""
Thresholding changes pixels' color values to a specified pixel value if the current pixel value
is less than a threshold value, which could be:

1. a specified global threshold value provided as an argument to the threshold function (simple thresholding),
2. the mean value of the pixels in the neighboring area (adaptive thresholding - mean method),
3. the weighted sum of neigborhood values where the weights are Gaussian windows (adaptive thresholding - Gaussian method).

The last two parameters to the adaptiveThreshold function are the size of the neighboring area and
the constant C which is subtracted from the mean or weighted mean calculated.
"""
MAX_THRESHOLD_VALUE = 255
BLOCK_SIZE = 15
THRESHOLD_CONSTANT = 0

# Filter image
filtered = cv.adaptiveThreshold(~grayscale, MAX_THRESHOLD_VALUE, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, BLOCK_SIZE, THRESHOLD_CONSTANT)

# =====================================================
# Isolating lines
"""
To isolate the vertical and horizontal lines, 

1. Set a scale.
2. Create a structuring element.
3. Isolate the lines by eroding and then dilating the image.
"""

horizontal = filtered.copy()
vertical = filtered.copy()

SCALE = 15

horizontal_size = int(horizontal.shape[1] / SCALE)
horizontal_structure = cv.getStructuringElement(cv.MORPH_RECT, (horizontal_size, 1))
utils.isolate_lines(horizontal, horizontal_structure)

vertical_size = int(vertical.shape[0] / SCALE)
vertical_structure = cv.getStructuringElement(cv.MORPH_RECT, (1, vertical_size))
utils.isolate_lines(vertical, vertical_structure)

# =====================================================
# Create mask with both horizontal and vertical lines
mask = horizontal + vertical

# Find contours
(_, contours, _) = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

# Find joints
joints = cv.bitwise_and(horizontal, vertical)

# =====================================================
MIN_TABLE_AREA = 100 # min table area to be considered a table
EPSILON = 3 # epsilon value for contour approximation
regions_of_interest = [] # list of possible tables
for i in range(len(contours)):
    area = cv.contourArea(contours[i])

    if (area < MIN_TABLE_AREA):
        continue

    # approxPolyDP approximates a polygonal curve within the specified precision
    curve = cv.approxPolyDP(contours[i], EPSILON, True)

    # boundingRect calculates the bounding rectangle of a point set (eg. a curve)
    rect = cv.boundingRect(curve) # format of each rect: x, y, w, h

    # Find the number of joints in each region of interest (ROI)
    # format: image_mat[rect.x: rect.x + rect.w, rect.y: rect.y + rect.h]
    joints_roi = joints[rect[1]:rect[1] + rect[3], rect[0]:rect[0] + rect[2]]
    (_, joints_contours, _) = cv.findContours(joints_roi, cv.RETR_CCOMP, cv.CHAIN_APPROX_SIMPLE)

    # Determines the number of corners in the image
    # If less than 5 corners, then the image
    # is likely not a table
    if len(joints_contours) < 5:
        continue

    regions_of_interest.append( resized[rect[1]:rect[1] + rect[3] , rect[0]:rect[0] + rect[2]] )
    
#    resized_copy = resized.copy()
#    cv.rectangle(resized_copy, (rect[0], rect[1]) , (rect[0] + rect[2], rect[1] + rect[3]) , (0, 255, 0), 1, 8, 0)

# =====================================================
# Extract tables
for i in range(len(regions_of_interest)):
    edges = cv.Canny(regions_of_interest[i], 200, 300, apertureSize = 3) # edge detection - edges include lines, curves, etc.
    lines = cv.HoughLinesP(edges, 1, np.pi/180, 120, minLineLength = 70, maxLineGap = 20) # line detection

    table_borders = []
    # print lines
    for j in range(len(lines)):
        table_borders.append(lines[j][0].tolist())

    (horizontal_borders, vertical_borders) = utils.sortLines(table_borders)

    for border in horizontal_borders:
        cv.line(regions_of_interest[i], (border[0], border[1]), (border[2], border[3]), (0, 0, 255), 2)

    for border in vertical_borders:
        cv.line(regions_of_interest[i], (border[0], border[1]), (border[2], border[3]), (0, 0, 255), 2)

    cv.imshow("roi", regions_of_interest[i])
    cv.waitKey(0)
    print()
