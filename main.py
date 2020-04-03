import numpy as np
import cv2 as cv
import utils
from table import Table
from PIL import Image
import xlsxwriter
import sys
from pdf2image import convert_from_path

# =====================================================
# IMAGE LOADING
# =====================================================
if len(sys.argv) < 2:
    print("Usage: python main.py <img_path>")
    sys.exit(1)

path = sys.argv[1]
if not path.endswith(".pdf") and not path.endswith(".jpg"):
    print("Must use a pdf or a jpg image to run the program.")
    sys.exit(1)

if path.endswith(".pdf"):
    ext_img = convert_from_path(path)[0]
else:
    ext_img = Image.open(path)

ext_img.save("data/target.png", "PNG")
image = cv.imread("data/target.png")

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
# and vertical lines in the image. Then find
# all contours in the mask.
mask = horizontal + vertical
(contours, _) = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

# Find intersections between the lines
# to determine if the intersections are table joints.
intersections = cv.bitwise_and(horizontal, vertical)

# Get tables from the images
tables = [] # list of tables
for i in range(len(contours)):
    # Verify that region of interest is a table
    (rect, table_joints) = utils.verify_table(contours[i], intersections)
    if rect == None or table_joints == None:
        continue

    # Create a new instance of a table
    table = Table(rect[0], rect[1], rect[2], rect[3])

    # Get an n-dimensional array of the coordinates of the table joints
    joint_coords = []
    for i in range(len(table_joints)):
        joint_coords.append(table_joints[i][0][0])
    joint_coords = np.asarray(joint_coords)

    # Returns indices of coordinates in sorted order
    # Sorts based on parameters (aka keys) starting from the last parameter, then second-to-last, etc
    sorted_indices = np.lexsort((joint_coords[:, 0], joint_coords[:, 1]))
    joint_coords = joint_coords[sorted_indices]

    # Store joint coordinates in the table instance
    table.set_joints(joint_coords)

    tables.append(table)

    #cv.rectangle(image, (table.x, table.y), (table.x + table.w, table.y + table.h), (0, 255, 0), 1, 8, 0)
    #cv.imshow("tables", image)
    #cv.waitKey(0)

# =====================================================
# OCR AND WRITING TEXT TO EXCEL
# =====================================================
out = "bin/"
table_name = "table.jpg"
psm = 6
oem = 3
mult = 3

utils.mkdir(out)
utils.mkdir("bin/table/")

utils.mkdir("excel/")
workbook = xlsxwriter.Workbook('excel/tables.xlsx')

for table in tables:
    worksheet = workbook.add_worksheet()

    table_entries = table.get_table_entries()

    table_roi = image[table.y:table.y + table.h, table.x:table.x + table.w]
    table_roi = cv.resize(table_roi, (table.w * mult, table.h * mult))

    cv.imwrite(out + table_name, table_roi)

    num_img = 0
    for i in range(len(table_entries)):
        row = table_entries[i]
        for j in range(len(row)):
            entry = row[j]
            entry_roi = table_roi[entry[1] * mult: (entry[1] + entry[3]) * mult, entry[0] * mult:(entry[0] + entry[2]) * mult]

            fname = out + "table/cell" + str(num_img) + ".jpg"
            cv.imwrite(fname, entry_roi)

            fname = utils.run_textcleaner(fname, num_img)
            text = utils.run_tesseract(fname, num_img, psm, oem)

            num_img += 1

            worksheet.write(i, j, text)

workbook.close()
