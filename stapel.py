"""
Solving my dad's stacking puzzle with linear programming.
(German "Stapel" = Stack)

Based on: The Looping Sudoku Problem Formulation for the PuLP Modeller
Authors: Antony Phillips, Dr Stuart Mitcehll
"""
# Import PuLP modeler functions
from pulp import *
import time

# The prob variable is created to contain the problem data
prob = LpProblem("Stapel Problem",LpMinimize)

# The arbitrary objective function is added
prob += 0, "Arbitrary Objective Function"


# A list of all positions
Positions = [str(i+1) for i in range(15)]
Orientations = ["1", "2", "3", "4"]

# A list of all sticks
Sticks = [str(i+1) for i in range(15)]

# Binary variables: Is stick s at position p with orientation o?
placements = LpVariable.dicts("Placement", (Sticks, Positions, Orientations), 0, 1, LpInteger)

# Each stick is at exactly one position & orientation
for s in Sticks:
    prob += lpSum([placements[s][p][o] for p in Positions for o in Orientations]) == 1, ""

# Each position has exactly one stick in one orientation
for p in Positions:
    prob += lpSum([placements[s][p][o] for s in Sticks for o in Orientations]) == 1, ""

# Now the complicated part starts. We need to encode the puzzle information.
# There are 9 * 4 = 36 touch points which each corresponds to a complicated
# equation.

# First, we should gather the information about all stick holes
#   1       2       3
#  ---------------------
#  ---------------------
#   4       5       6
# This is orientation "1", there are three other orientations
#       321         456         654
# "2":  ---  "3":   ---  "4":   ---
#       654         123         321
# A "0" indicates a hole and a "1" indicates no hole.
stick_shape = {
    "1": ["1", 1, 1, 1, 1, 1, 1],
    "2": ["1", 1, 1, 1, 1, 0, 1],
    "3": ["1", 1, 0, 1, 1, 1, 1],
    "4": ["1", 0, 0, 0, 0, 0, 0],
    "5": ["1", 0, 1, 0, 0, 0, 0],
    "6": ["1", 0, 0, 1, 1, 1, 1],
    "7": ["1", 0, 1, 0, 0, 1, 1],
    "8": ["1", 0, 0, 0, 1, 1, 1],
    "9": ["1", 1, 0, 1, 1, 1, 1],
    "10": ["1", 1, 0, 1, 1, 1, 0],
    "11": ["1", 0, 1, 0, 1, 0, 1],
    "12": ["1", 0, 1, 0, 1, 1, 1],
    "13": ["1", 0, 1, 1, 1, 1, 0],
    "14": ["1", 0, 0, 1, 1, 1, 1],
    "15": ["1", 0, 1, 0, 1, 0, 1]
}

# TODO: This can be a lot more concise.
def vs_all_orientations(s, p, notch):
    result = []
    if notch == 1:
        if stick_shape[s][1]:
            result.append(placements[s][p]["1"])
        if stick_shape[s][3]:
            result.append(placements[s][p]["2"])
        if stick_shape[s][4]:
            result.append(placements[s][p]["3"])
        if stick_shape[s][6]:
            result.append(placements[s][p]["4"])
        return result
    elif notch == 2:
        if stick_shape[s][2]:
            result.append(placements[s][p]["1"])
            result.append(placements[s][p]["2"])
        if stick_shape[s][5]:
            result.append(placements[s][p]["3"])
            result.append(placements[s][p]["4"])
        return result
    if notch == 3:
        if stick_shape[s][3]:
            result.append(placements[s][p]["1"])
        if stick_shape[s][1]:
            result.append(placements[s][p]["2"])
        if stick_shape[s][6]:
            result.append(placements[s][p]["3"])
        if stick_shape[s][4]:
            result.append(placements[s][p]["4"])
        return result
    if notch == 4:
        if stick_shape[s][4]:
            result.append(placements[s][p]["1"])
        if stick_shape[s][6]:
            result.append(placements[s][p]["2"])
        if stick_shape[s][1]:
            result.append(placements[s][p]["3"])
        if stick_shape[s][3]:
            result.append(placements[s][p]["4"])
        return result
    elif notch == 5:
        if stick_shape[s][5]:
            result.append(placements[s][p]["1"])
            result.append(placements[s][p]["2"])
        if stick_shape[s][2]:
            result.append(placements[s][p]["3"])
            result.append(placements[s][p]["4"])
        return result
    if notch == 6:
        if stick_shape[s][6]:
            result.append(placements[s][p]["1"])
        if stick_shape[s][4]:
            result.append(placements[s][p]["2"])
        if stick_shape[s][3]:
            result.append(placements[s][p]["3"])
        if stick_shape[s][1]:
            result.append(placements[s][p]["4"])
        return result


def touch_point_constraint(p1, n1, p2, n2):
    global prob
    vs = [] # variables
    for s in Sticks:
        vs.extend(vs_all_orientations(s, p1, n1))
        vs.extend(vs_all_orientations(s, p2, n2))
    prob += lpSum(vs) == 1, ""


# TODO: While this is "rather compact" I can still condense it down.
# First layer
touch_point_constraint("1", 1, "4", 4)
touch_point_constraint("1", 2, "5", 4)
touch_point_constraint("1", 3, "6", 4)
touch_point_constraint("2", 1, "4", 5)
touch_point_constraint("2", 2, "5", 5)
touch_point_constraint("2", 3, "6", 5)
touch_point_constraint("3", 1, "4", 6)
touch_point_constraint("3", 2, "5", 6)
touch_point_constraint("3", 3, "6", 6)

# Second layer
touch_point_constraint("4", 1, "7", 4)
touch_point_constraint("5", 1, "7", 5)
touch_point_constraint("6", 1, "7", 6)
touch_point_constraint("4", 2, "8", 4)
touch_point_constraint("5", 2, "8", 5)
touch_point_constraint("6", 2, "8", 6)
touch_point_constraint("4", 3, "9", 4)
touch_point_constraint("5", 3, "9", 5)
touch_point_constraint("6", 3, "9", 6)

# Third layer
touch_point_constraint("7", 1, "10", 4)
touch_point_constraint("7", 2, "11", 4)
touch_point_constraint("7", 3, "12", 4)
touch_point_constraint("8", 1, "10", 5)
touch_point_constraint("8", 2, "11", 5)
touch_point_constraint("8", 3, "12", 5)
touch_point_constraint("9", 1, "10", 6)
touch_point_constraint("9", 2, "11", 6)
touch_point_constraint("9", 3, "12", 6)

# Fourth layer
touch_point_constraint("10", 1, "13", 4)
touch_point_constraint("11", 1, "13", 5)
touch_point_constraint("12", 1, "13", 6)
touch_point_constraint("10", 2, "14", 4)
touch_point_constraint("11", 2, "14", 5)
touch_point_constraint("12", 2, "14", 6)
touch_point_constraint("10", 3, "15", 4)
touch_point_constraint("11", 3, "15", 5)
touch_point_constraint("12", 3, "15", 6)



# The problem data is written to an .lp file
start = time.time()
prob.writeLP("Stapel.lp")

# A file called sudokuout.txt is created/overwritten for writing to
# sudokuout = open('sudokuout.txt','w')

prob.solve()

for s in Sticks:
    for p in Positions:
        for o in Orientations:
            if value(placements[s][p][o]) == 1:
                print(s, p, o)

end = time.time()
print(end - start)

# Add an option to list all possible solutions.