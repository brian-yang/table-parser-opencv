import cv2 as cv
import pytesseract as tess
from PIL import Image
import subprocess as s
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
MIN_TABLE_AREA = 50 # min table area to be considered a table
EPSILON = 3 # epsilon value for contour approximation
def verify_table(contour, intersections):
    area = cv.contourArea(contour)

    if (area < MIN_TABLE_AREA):
        return (None, None)

    # approxPolyDP approximates a polygonal curve within the specified precision
    curve = cv.approxPolyDP(contour, EPSILON, True)

    # boundingRect calculates the bounding rectangle of a point set (eg. a curve)
    rect = cv.boundingRect(curve) # format of each rect: x, y, w, h

    # Finds the number of joints in each region of interest (ROI)
    # Format is in row-column order (as finding the ROI involves numpy arrays)
    # format: image_mat[rect.y: rect.y + rect.h, rect.x: rect.x + rect.w]
    possible_table_region = intersections[rect[1]:rect[1] + rect[3], rect[0]:rect[0] + rect[2]]
    (possible_table_joints, _) = cv.findContours(possible_table_region, cv.RETR_CCOMP, cv.CHAIN_APPROX_SIMPLE)

    # Determines the number of table joints in the image
    # If less than 5 table joints, then the image
    # is likely not a table
    if len(possible_table_joints) < 5:
        return (None, None)

    return rect, possible_table_joints

"""
Creates the build directory if it doesn't already exist."
"""
def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)

"""
Displays an image with opencv for durationMillis milliseconds
"""
def showImg(name, matrix, durationMillis = 0):
    cv.imshow(name, matrix)
    cv.waitKey(durationMillis)

"""
Clean the image by using the textcleaner script
"""
def run_textcleaner(filename, img_id):
    mkdir("bin/cleaned/")

    # Run textcleaner
    cleaned_file = "bin/cleaned/cleaned" + str(img_id) + ".jpg"
    s.call(["./textcleaner", "-g", "-e", "none", "-f", str(10), "-o", str(5), filename, cleaned_file])

    return cleaned_file

"""
Run tesseract to perform optical character recognition (OCR)
"""
def run_tesseract(filename, img_id, psm, oem):
    mkdir("bin/extracted/")

    image = Image.open(filename)
    language = 'eng'
    configuration = "--psm " + str(psm) + " --oem " + str(oem)

    # Run tesseract
    text = tess.image_to_string(image, lang=language, config=configuration)
    if len(text.strip()) == 0:
        configuration += " -c tessedit_char_whitelist=0123456789"
        text = tess.image_to_string(image, lang=language, config=configuration)
    #print(text)

    return text
