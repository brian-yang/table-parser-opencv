import numpy as np
import cv2 as cv

# load the table image
image = cv.imread("table.jpg")

# Resize image
# size = (800, 900) # rows and columns in image
# resized = cv.resize(image, size)
resized = image.copy()

# Convert resized image to grayscale
if len(image.shape) == 3:
	# print "Image has 3 channels"
	grayscale_img = cv.cvtColor(resized, cv.COLOR_BGR2GRAY)

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
size_of_neighbors = 15
threshold_constant = 0
filtered = cv.adaptiveThreshold(~grayscale_img, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, size_of_neighbors, threshold_constant)

# =====================================================
horizontal = filtered.copy()
vertical = filtered.copy()

scale = 15

# apply morphology operations
def isolate_lines(src, structuring_element):
        cv.erode(src, structuring_element, src, (-1, -1)) # makes white spots smaller
        cv.dilate(src, structuring_element, src, (-1, -1)) # makes white spots bigger

horizontal_size = horizontal.shape[1] / scale
# create structure element
horizontal_structure = cv.getStructuringElement(cv.MORPH_RECT, (horizontal_size, 1))
# isolate lines
isolate_lines(horizontal, horizontal_structure)

vertical_size = vertical.shape[0] / scale
# create structure element
vertical_structure = cv.getStructuringElement(cv.MORPH_RECT, (1, vertical_size))
# isolate lines
isolate_lines(vertical, vertical_structure)
# =====================================================
# Create mask with both horizontal and vertical lines
mask = horizontal + vertical

# Find joints
joints = cv.bitwise_and(horizontal, vertical)

# Find contours
(_, contours, _) = cv.findContours(mask.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
# =====================================================
contours_poly = []
bound_rect = []
regions_of_interest = []
MIN_TABLE_AREA = 100
EPSILON = 3
for i in range(len(contours)):
        area = cv.contourArea(contours[i])

        if (area < MIN_TABLE_AREA):
                continue

        contours_poly.append(cv.approxPolyDP(contours[i], EPSILON, True))
        bound_rect.append(cv.boundingRect(contours_poly[i])) # format of each rect: x, y, w, h

        # Find the number of joints each table has by finding the region of interest (ROI)
        # format: image_mat[rect.x: rect.x + rect.w, rect.y: rect.y + rect.h]
        joints_copy = joints.copy()
        roi = joints_copy[bound_rect[i][1]:bound_rect[i][1] + bound_rect[i][3] , bound_rect[i][0]:bound_rect[i][0] + bound_rect[i][2]]

        (_, joints_contours, _) = cv.findContours(roi, cv.RETR_CCOMP, cv.CHAIN_APPROX_SIMPLE)

        # Determins the number of corners in the image
        # If less than 5 corners, then the image
        # is likely not a table
        if len(joints_contours) < 5:
                continue

        resized_copy = resized.copy()
        regions_of_interest.append( (resized_copy[bound_rect[i][1]:bound_rect[i][1] + bound_rect[i][3] , bound_rect[i][0]:bound_rect[i][0] + bound_rect[i][2]]).copy() )

        cv.rectangle(resized, (bound_rect[i][0], bound_rect[i][1]) , (bound_rect[i][0] + bound_rect[i][2], bound_rect[i][1] + bound_rect[i][3]) , (0, 255, 0), 1, 8, 0)

# =====================================================
# Extract tables
for i in range(len(regions_of_interest)):
        edges = cv.Canny(regions_of_interest[i], 200, 300, apertureSize = 3) # edge detection
        lines = cv.HoughLinesP(edges, 1, np.pi/180, 120, minLineLength = 70, maxLineGap = 20)

        # print lines
        for j in range(len(lines)):
                l = lines[j][0].tolist()
                print l
                cv.line(regions_of_interest[i], (l[0], l[1]), (l[2], l[3]), (0, 0, 255), 2)

        cv.imshow("roi", regions_of_interest[i])
        cv.waitKey(0)

# =====================================================
# cv.imshow("resized", resized)
# cv.waitKey(0)
