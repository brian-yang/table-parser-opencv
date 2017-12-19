import cv2 as cv

# Apply morphology operations
def isolate_lines(src, structuring_element):
	cv.erode(src, structuring_element, src, (-1, -1)) # makes white spots smaller
	cv.dilate(src, structuring_element, src, (-1, -1)) # makes white spots bigger

# Remove duplicate horizontal and vertical lines
DISTANCE_THRESHOLD = 3
def removeDuplicates(lines):
    for i in range(len(lines)):
        for j in range(i + 1, len(lines)):
            if j >= len(lines):
                continue

            score = 0
            for coord in range(len(lines[i])):
                if abs(lines[i][coord] - lines[j][coord]) <= DISTANCE_THRESHOLD:
                    score += 1

            if score == len(lines[i]):
                lines.pop(j)

# Get the horizontal and vertical lines in the table image
def sortLines(lines):
    horizontal_lines= []
    vertical_lines = []

    for i in range(len(lines)):
        # first check if the line is horizontal or vertical
        if abs(lines[i][0] - lines[i][2]) < 2:
            vertical_lines.append(lines[i])
        elif abs(lines[i][1] - lines[i][3]) < 2:
            horizontal_lines.append(lines[i])

    removeDuplicates(horizontal_lines)
    removeDuplicates(vertical_lines)

    return horizontal_lines, vertical_lines


