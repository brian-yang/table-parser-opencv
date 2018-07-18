import cv2 as cv
import os

"""
Apply morphology operations
"""
def isolate_lines(src, structuring_element):
	cv.erode(src, structuring_element, src, (-1, -1)) # makes white spots smaller
	cv.dilate(src, structuring_element, src, (-1, -1)) # makes white spots bigger

"""
Verify if the region inside a contour is a table
If it is a table, returns the bounding rect
and the table joints. Else return None.
"""
MIN_TABLE_AREA = 100 # min table area to be considered a table
EPSILON = 3 # epsilon value for contour approximation
def verify_table(contour, intersections):
    area = cv.contourArea(contour)

    if (area < MIN_TABLE_AREA):
        return None

    # approxPolyDP approximates a polygonal curve within the specified precision
    curve = cv.approxPolyDP(contour, EPSILON, True)

    # boundingRect calculates the bounding rectangle of a point set (eg. a curve)
    rect = cv.boundingRect(curve) # format of each rect: x, y, w, h

    # Finds the number of joints in each region of interest (ROI)
    # Format is in row-column order (as finding the ROI involves numpy arrays)
    # format: image_mat[rect.y: rect.y + rect.h, rect.x: rect.x + rect.w]
    possible_table_region = intersections[rect[1]:rect[1] + rect[3], rect[0]:rect[0] + rect[2]]
    (_, possible_table_joints, _) = cv.findContours(possible_table_region, cv.RETR_CCOMP, cv.CHAIN_APPROX_SIMPLE)

    # Determines the number of table joints in the image
    # If less than 5 table joints, then the image
    # is likely not a table
    if len(possible_table_joints) < 5:
        return None

    return rect, possible_table_joints

"""
Creates the build directory if it doesn't already exist."
"""
def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)

## Remove duplicate horizontal and vertical lines
#DISTANCE_THRESHOLD = 3
#def remove_duplicates(lines):
#    for i in range(len(lines)):
#        for j in range(i + 1, len(lines)):
#            if j >= len(lines):
#                continue
#
#            score = 0
#            for coord in range(len(lines[i])):
#                if abs(lines[i][coord] - lines[j][coord]) <= DISTANCE_THRESHOLD:
#                    score += 1
#
#            if score == len(lines[i]):
#                lines.pop(j)
#
## Get the horizontal and vertical lines in the table image
#def sort_lines(lines):
#    horizontal_lines= []
#    vertical_lines = []
#
#    for i in range(len(lines)):
#        # first check if the line is horizontal or vertical
#        if abs(lines[i][0] - lines[i][2]) < 2:
#            vertical_lines.append(lines[i])
#        elif abs(lines[i][1] - lines[i][3]) < 2:
#            horizontal_lines.append(lines[i])
#
#    removeDuplicates(horizontal_lines)
#    removeDuplicates(vertical_lines)
#
#    return horizontal_lines, vertical_lines


