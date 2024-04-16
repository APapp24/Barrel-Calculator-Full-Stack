#!/usr/bin/env python
# coding: utf-8

# In[ ]:

# Import required modules for linear programming and randomness
from pulp import LpProblem, LpVariable, lpSum, LpMinimize, LpStatus, PULP_CBC_CMD
import random

class Barrel:
    def __init__(self, number, x_percent, y_percent, z_percent, w_percent, v_percent):
        self.number = number
        self.x_percent = x_percent
        self.y_percent = y_percent
        self.z_percent = z_percent
        self.w_percent = w_percent
        self.v_percent = v_percent

class Target:
    def __init__(self, weight, x_range, y_range, z_range, w_range, v_range):
        self.x_range = x_range
        self.y_range = y_range
        self.z_range = z_range
        self.w_range = w_range
        self.v_range = v_range
        self.weight = weight


def input_collector():
    barrel_number = int(input('How many barrels? '))
    barrel_list = []
    for n in range(barrel_number):
        number = n + 1
        x_percent = float(input(f'X percent of barrel #{number}? '))
        y_percent = float(input(f'Y percent of barrel #{number}? '))
        z_percent = float(input(f'Z percent of barrel #{number}? '))
        w_percent = float(input(f'W percent of barrel #{number}? '))
        v_percent = float(input(f'V percent of barrel #{number}? '))
        print()
        barrel_list.append(Barrel(number, x_percent, y_percent, z_percent, w_percent, v_percent))

    target_weight = float(input("Weight of the target amount? "))

    target_x_min = float(input("Minimum target percentage for X? "))
    target_x_max = float(input("Maximum target percentage for X? "))
    target_x_range = (target_x_min, target_x_max)

    target_y_min = float(input("Minimum target percentage for Y? "))
    target_y_max = float(input("Maximum target percentage for Y? "))
    target_y_range = (target_y_min, target_y_max)

    target_z_min = float(input("Minimum target percentage for Z? "))
    target_z_max = float(input("Maximum target percentage for Z? "))
    target_z_range = (target_z_min, target_z_max)

    target_w_min = float(input("Minimum target percentage for W? "))
    target_w_max = float(input("Maximum target percentage for W? "))
    target_w_range = (target_w_min, target_w_max)

    target_v_min = float(input("Minimum target percentage for V? "))
    target_v_max = float(input("Maximum target percentage for V? "))
    target_v_range = (target_v_min, target_v_max)

    return barrel_list, Target(target_weight, target_x_range, target_y_range, target_z_range, target_w_range, target_v_range)

def find_solutions(barrels, target):
    model = LpProblem(name="barrel-mixing", sense=LpMinimize)
    x = [LpVariable(f'x_{i}', lowBound=0, cat='Continuous') for i in range(len(barrels))]

    # Objective: Match the target weight
    model += lpSum(x[i] for i in range(len(barrels))) == target.weight, "total_weight"

    fudge_factor = 2.0  # 2 percent fudge factor

    for constraint_name, target_range, barrel_percent in [
        ("x", target.x_range, [barrel.x_percent for barrel in barrels]),
        ("y", target.y_range, [barrel.y_percent for barrel in barrels]),
        ("z", target.z_range, [barrel.z_percent for barrel in barrels]),
        ("w", target.w_range, [barrel.w_percent for barrel in barrels]),
        ("v", target.v_range, [barrel.v_percent for barrel in barrels])
    ]:
        min_range = target_range[0] - fudge_factor
        max_range = target_range[1] + fudge_factor

        model += lpSum(x[i] * barrel_percent[i] / 100 for i in range(len(barrels))) >= target.weight * min_range / 100, f"{constraint_name}_composition_min"
        model += lpSum(x[i] * barrel_percent[i] / 100 for i in range(len(barrels))) <= target.weight * max_range / 100, f"{constraint_name}_composition_max"

    status = model.solve(PULP_CBC_CMD(msg=0))

    if LpStatus[status] == 'Optimal':
        solution = [(var.varValue, barrels[i].number) for i, var in enumerate(x)]
        logger.info("Debug: Solution Generated: %s", solution)  # Debug step 1
        return solution
    else:
        return None


def generate_targets(weight, x_range, y_range, z_range, w_range, v_range, num_targets=500):
    targets = []
    for _ in range(num_targets):
        x_val = random.uniform(*x_range)
        y_val = random.uniform(*y_range)
        z_val = random.uniform(*z_range)
        w_val = random.uniform(*w_range)
        v_val = random.uniform(*v_range)

        # Sum of all the picked random values
        total = x_val + y_val + z_val + w_val + v_val

        # Normalizing the values so they sum up to 100
        x_val = (x_val / total) * 100
        y_val = (y_val / total) * 100
        z_val = (z_val / total) * 100
        w_val = (w_val / total) * 100
        v_val = (v_val / total) * 100

        targets.append(Target(weight, (x_val, x_val), (y_val, y_val), (z_val, z_val), (w_val, w_val), (v_val, v_val)))

    return targets

def calculate_concentrations(solution, barrels):

    total_x = sum(weight * barrels[i-1].x_percent / 100 for weight, i in solution)
    total_y = sum(weight * barrels[i-1].y_percent / 100 for weight, i in solution)
    total_z = sum(weight * barrels[i-1].z_percent / 100 for weight, i in solution)
    total_w = sum(weight * barrels[i-1].w_percent / 100 for weight, i in solution)
    total_v = sum(weight * barrels[i-1].v_percent / 100 for weight, i in solution)

    total_weight = sum(weight for weight, _ in solution)

    percentage_x = (total_x / total_weight) * 100
    percentage_y = (total_y / total_weight) * 100
    percentage_z = (total_z / total_weight) * 100
    percentage_w = (total_w / total_weight) * 100
    percentage_v = (total_v / total_weight) * 100

    print(f"A solution has been found with the following composition:")
    print(f"{percentage_x:.2f}% of X, {percentage_y:.2f}% of Y, {percentage_z:.2f}% of Z, {percentage_w:.2f}% of W, {percentage_v:.2f}% of V")


def main():
    barrels, target_ranges = input_collector()
    targets = generate_targets(target_ranges.weight, target_ranges.x_range, target_ranges.y_range,
                               target_ranges.z_range, target_ranges.w_range, target_ranges.v_range)

    print("Debug: Barrels:", barrels)

    solutions = []
    solution_count = 0  # Initialize counter for solutions
    for target in targets:
        if solution_count >= 10:  # Stop after finding 10 solutions
            break
        solution = find_solutions(barrels, target)
        if solution:
            solutions.append((solution, target))
            solution_count += 1  # Increment counter when a solution is found

    for i, (solution, target) in enumerate(solutions):
        print()
        print(f"Solution {i + 1} for target with weight {target.weight}:")
        for j, (weight, barrel_number) in enumerate(solution):
            if weight > 0:
                print(f"Take {weight} pounds from barrel {barrel_number}")
        calculate_concentrations(solution, barrels)

if __name__ == "__main__":
    main()

