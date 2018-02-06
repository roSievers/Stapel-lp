"""
Solving my dad's stacking puzzle with linear programming.
(German "Stapel" = Stack)

Based on: The Looping Sudoku Problem Formulation for the PuLP Modeller
Authors: Antony Phillips, Dr Stuart Mitcehll
"""
# Import PuLP modeler functions
from pulp import *
import time

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
# The first number (in a 1-tuple) counts how many sticks of this kind exist.
stick_shape = {
    "1":  [(1,), 1, 1, 1, 1, 1, 1],
    "2":  [(3,), 1, 0, 1, 1, 1, 1], # There are three of this Stick available
    "3":  [(1,), 1, 0, 1, 1, 1, 0],
    "4":  [(1,), 0, 1, 1, 1, 1, 0],
    "5":  [(1,), 0, 1, 0, 1, 1, 1],
    "6":  [(2,), 0, 1, 0, 1, 0, 1],
    "7":  [(1,), 0, 1, 0, 0, 0, 0],
    "8":  [(1,), 0, 1, 0, 0, 1, 1],
    "9":  [(2,), 0, 0, 1, 1, 1, 1],
    "10": [(1,), 0, 0, 0, 1, 1, 1],
    "11": [(1,), 0, 0, 0, 0, 0, 0]
}

# A list of all positions
Positions = [str(i+1) for i in range(15)]
Orientations = ["1", "2", "3", "4"]

# A list of all sticks
Sticks = [str(i+1) for i in range(len(stick_shape))]

# TODO: This can be a lot more concise.
def vs_all_orientations(placements, s, p, notch):
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

def touch_point_constraint(prob, placements, p1, n1, p2, n2):
    vs = [] # variables
    for s in Sticks:
        vs.extend(vs_all_orientations(placements, s, p1, n1))
        vs.extend(vs_all_orientations(placements, s, p2, n2))
    prob += lpSum(vs) == 1, ""

def generate_problem_statement():
    # The prob variable is created to contain the problem data
    prob = LpProblem("Stapel Problem",LpMinimize)

    # The arbitrary objective function is added
    prob += 0, "Arbitrary Objective Function"

    # Binary variables: Is stick s at position p with orientation o?
    placements = LpVariable.dicts("Placement", (Sticks, Positions, Orientations), 0, 1, LpInteger)

    # Count sticks and make sure they are used as often as they are available.
    for s in Sticks:
        prob += lpSum([placements[s][p][o] for p in Positions for o in Orientations]) == stick_shape[s][0][0], ""

    # Each position has exactly one stick in one orientation
    for p in Positions:
        prob += lpSum([placements[s][p][o] for s in Sticks for o in Orientations]) == 1, ""

    # TODO: While this is "rather compact" I can still condense it down.
    # First layer
    touch_point_constraint(prob, placements, "1", 1, "4", 4)
    touch_point_constraint(prob, placements, "1", 2, "5", 4)
    touch_point_constraint(prob, placements, "1", 3, "6", 4)
    touch_point_constraint(prob, placements, "2", 1, "4", 5)
    touch_point_constraint(prob, placements, "2", 2, "5", 5)
    touch_point_constraint(prob, placements, "2", 3, "6", 5)
    touch_point_constraint(prob, placements, "3", 1, "4", 6)
    touch_point_constraint(prob, placements, "3", 2, "5", 6)
    touch_point_constraint(prob, placements, "3", 3, "6", 6)

    # Second layer
    touch_point_constraint(prob, placements, "4", 1, "7", 4)
    touch_point_constraint(prob, placements, "5", 1, "7", 5)
    touch_point_constraint(prob, placements, "6", 1, "7", 6)
    touch_point_constraint(prob, placements, "4", 2, "8", 4)
    touch_point_constraint(prob, placements, "5", 2, "8", 5)
    touch_point_constraint(prob, placements, "6", 2, "8", 6)
    touch_point_constraint(prob, placements, "4", 3, "9", 4)
    touch_point_constraint(prob, placements, "5", 3, "9", 5)
    touch_point_constraint(prob, placements, "6", 3, "9", 6)

    # Third layer
    touch_point_constraint(prob, placements, "7", 1, "10", 4)
    touch_point_constraint(prob, placements, "7", 2, "11", 4)
    touch_point_constraint(prob, placements, "7", 3, "12", 4)
    touch_point_constraint(prob, placements, "8", 1, "10", 5)
    touch_point_constraint(prob, placements, "8", 2, "11", 5)
    touch_point_constraint(prob, placements, "8", 3, "12", 5)
    touch_point_constraint(prob, placements, "9", 1, "10", 6)
    touch_point_constraint(prob, placements, "9", 2, "11", 6)
    touch_point_constraint(prob, placements, "9", 3, "12", 6)

    # Fourth layer
    touch_point_constraint(prob, placements, "10", 1, "13", 4)
    touch_point_constraint(prob, placements, "11", 1, "13", 5)
    touch_point_constraint(prob, placements, "12", 1, "13", 6)
    touch_point_constraint(prob, placements, "10", 2, "14", 4)
    touch_point_constraint(prob, placements, "11", 2, "14", 5)
    touch_point_constraint(prob, placements, "12", 2, "14", 6)
    touch_point_constraint(prob, placements, "10", 3, "15", 4)
    touch_point_constraint(prob, placements, "11", 3, "15", 5)
    touch_point_constraint(prob, placements, "12", 3, "15", 6)

    return prob, placements

start = time.time()

prob, placements = generate_problem_statement()

# prob += placements["2"]["1"]["1"] == 1, "Initial setup condition."

# prob += placements["1"]["1"]["1"] == 1, "Initial setup condition."
# prob += placements["2"]["2"]["1"] == 1, ""
# prob += placements["9"]["3"]["1"] == 1, ""

# The problem data is written to an .lp file
prob.writeLP("Stapel.lp")

prob.solve()

end = time.time()
print("Time:", end - start)

def stick_string(stick_format):
    def notch_down_string(not_a_notch):
        if not_a_notch:
            return "--"
        else:
            return "\\/"
    def notch_up_string(not_a_notch):
        if not_a_notch:
            return "--"
        else:
            return "/\\"
    # stick_format must be a value from stick_shape.
    return (f"--{notch_down_string(stick_format[1])}--{notch_down_string(stick_format[2])}--{notch_down_string(stick_format[3])}--\n" +
           f"--{notch_up_string(stick_format[4])}--{notch_up_string(stick_format[5])}--{notch_up_string(stick_format[6])}--")

if LpStatus[prob.status] == "Optimal":
    print("Solution found: (Stick, Position, Orientation)")
    for p in Positions:
        for s in Sticks:
            for o in Orientations:
                if value(placements[s][p][o]) == 1:
                    print(s, p, o)
                    print(stick_string(stick_shape[s]))
else:
    print("Status:", LpStatus[prob.status])

