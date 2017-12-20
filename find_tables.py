import numpy as np
import cv2 as cv
import utils
from table import Table

# =====================================================
# IMAGE LOADING
# =====================================================
# Load the image
folder = "data/"
image = cv.imread(folder + "table.jpg")

# Resize image
# size = (800, 900) # rows and columns in image
# resized = cv.resize(image, size)

# Convert resized RGB image to grayscale
NUM_CHANNELS = 3
if len(image.shape) == NUM_CHANNELS:
    grayscale = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

# =====================================================
# IMAGE FILTERING (using adaptive thresholding)
# =====================================================
"""
ADAPTIVE THRESHOLDING
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
# LINE ISOLATION
# =====================================================
"""
HORIZONTAL AND VERTICAL LINE ISOLATION
To isolate the vertical and horizontal lines, 

1. Set a scale.
2. Create a structuring element.
3. Isolate the lines by eroding and then dilating the image.
"""
SCALE = 15

# Isolate horizontal and vertical lines using morphological operations
horizontal = filtered.copy()
vertical = filtered.copy()

horizontal_size = int(horizontal.shape[1] / SCALE)
horizontal_structure = cv.getStructuringElement(cv.MORPH_RECT, (horizontal_size, 1))
utils.isolate_lines(horizontal, horizontal_structure)

vertical_size = int(vertical.shape[0] / SCALE)
vertical_structure = cv.getStructuringElement(cv.MORPH_RECT, (1, vertical_size))
utils.isolate_lines(vertical, vertical_structure)

# =====================================================
# TABLE EXTRACTION
# =====================================================
# Create an image mask with just the horizontal 
# and vertical lines in the image
mask = horizontal + vertical

# Find all contours in the mask
(_, contours, _) = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

# Find intersections between the lines
intersections = cv.bitwise_and(horizontal, vertical)

# Extract tables
tables = [] # list of tables
for i in range(len(contours)):
    (rect, table_joints) = utils.verify_table(contours[i], intersections)

    # Store the table images in a list
    table = Table(rect[0], rect[1], rect[2], rect[3])
    tables.append(table)

    # Get an n-dimensional array of the coordinates of the table joints
    joint_coords = []
    for i in range(len(table_joints)):
        joint_coords.append(table_joints[i][0][0])
    joint_coords = np.asarray(joint_coords)
    table.joints = joint_coords

    print(table.joints)

    cv.rectangle(image, (table.x, table.y), (table.x + table.w, table.y + table.h), (0, 255, 0), 1, 8, 0)
    cv.imshow("tables", image)
    cv.waitKey(0)

# Identify table borders on tables
#for i in range(len(regions_of_interest)):
#    edges = cv.Canny(regions_of_interest[i], 200, 300, apertureSize = 3) # edge detection - edges include lines, curves, etc.
#    lines = cv.HoughLinesP(edges, 1, np.pi/180, 120, minLineLength = 70, maxLineGap = 20) # line detection
#
#    table_borders = []
#    # print lines
#    for j in range(len(lines)):
#        table_borders.append(lines[j][0].tolist())
#
#    (horizontal_borders, vertical_borders) = utils.sortLines(table_borders)
#
#    for border in horizontal_borders:
#        cv.line(regions_of_interest[i], (border[0], border[1]), (border[2], border[3]), (0, 0, 255), 2)
#
#    for border in vertical_borders:
#        cv.line(regions_of_interest[i], (border[0], border[1]), (border[2], border[3]), (0, 0, 255), 2)
#
#    cv.imshow("roi", regions_of_interest[i])
#    cv.waitKey(0)
#    print()
