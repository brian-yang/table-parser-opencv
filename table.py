class Table:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.joints = None

    def __str__(self):
        return "(x: %d, y: %d, w: %d, h: %d)" % (self.x, self.x + self.w, self.y, self.y + self.h)
    
    # Stores the coordinates of the table joints.
    # Assumes the n-dimensional array joints is sorted in ascending order.
    def set_joints(self, joints):
        if self.joints != None:
            raise ValueError("Invalid setting of table joints array.")

        self.joints = []
        row_y = joints[0][1]
        row = []
        for i in range(len(joints)):
            if i == len(joints) - 1:
                row.append(joints[i])
                self.joints.append(row)
                break

            row.append(joints[i])

            # If the next joint has a new y-coordinate,
            # start a new row.
            if joints[i + 1][1] != row_y:
                self.joints.append(row)
                row_y = joints[i + 1][1]
                row = []

    # Prints the coordinates of the joints.
    def print_joints(self):
        if self.joints == None:
            print("Joint coordinates not found.")
            return

        print("[")
        for row in self.joints:
            print(row)
        print("]")

    # Finds table entries by using the coordinates
    # of the table joints to find the ROI of each table entry in the table image.
    def get_table_entries(self):
        if self.joints == None:
            print("Joint coordinates not found.")
            return

        entry_coords = []
        for i in range(0, len(self.joints) - 1):
            entry_coords.append(self.get_entry_bounds_in_row(self.joints[i], self.joints[i + 1]))

        return entry_coords

    # Finds the bounds of each table entry ROI
    # in each row based on the given sets of joints.
    def get_entry_bounds_in_row(self, joints_A, joints_B):
        row_entries = []

        # Since the sets of joints may not have
        # the same number of points
        # we pick a set to define the row by.
        if len(joints_A) <= len(joints_B):
            defining_joints = joints_A
            helper_joints = joints_B
        else:
            defining_joints = joints_B
            helper_joints = joints_A

        for i in range(0, len(defining_joints) - 1):
            x = defining_joints[i][0]
            y = defining_joints[i][1]
            w = defining_joints[i + 1][0] - x # helper_joints's (i + 1)th coordinate may not be the lower-right corner
            h = abs(helper_joints[0][1] - y) # helper_joints has the same y-coordinate for all of its elements
            row_entries.append([x, y, w, h])

        return row_entries
