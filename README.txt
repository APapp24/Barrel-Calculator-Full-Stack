****************************************
*****************readme*****************
****************************************
Size_5_Barrel_Calculator_With_Range.py:
The code aims to solve a linear programming problem related to mixing different barrels to meet a set of target percentages for various constituents (X, Y, Z, W, V). The problem is solved using Python's PuLP library, and the program can handle an arbitrary number of barrels and a range of target percentages.

Classes and Data Collection:

    Barrel and Target classes store attributes of barrels and target mixtures respectively.
    input_collector() function collects input for the number of barrels and their attributes, as well as the target attributes.

Optimization and Constraints:

    find_solutions() sets up the linear programming model. It minimizes the total weight of barrels used while meeting the composition constraints.
    Objective Function: Match the target weight by summing up the weights of the barrels.
    Constraints: It enforces the minimum and maximum percentages for X, Y, Z, W, and V within a 2% 'fudge factor'.
    The function returns a list of weight from each barrel if an optimal solution is found.

Random Target Generation:

    generate_targets() generates a list of random target mixtures within the provided ranges. The random values are then normalized to sum up to 100%.

Solution Calculation:

    calculate_concentrations() takes a solution and calculates the final composition of X, Y, Z, W, and V in percentages.

Main Loop:

    main() acts as the control flow. It collects inputs, generates random targets, finds solutions, and displays them.
    It stops after finding 10 solutions and offers the user to calculate again.

The program thus provides a comprehensive, iterative approach to solve a multi-dimensional barrel mixing problem using linear programming.

    Barrel & Target Classes:
        Barrel class: Stores attributes like number and percentages (x_percent, y_percent, etc.) for each barrel.
        Target class: Contains weight and range of acceptable percentages (x_range, y_range, etc.) for the target mixture.

    input_collector():
        Collects user inputs for the number and characteristics of barrels and the target attributes.
        Returns a list of Barrel objects and a Target object.

    find_solutions():
        Initializes a linear programming model (LpProblem) aiming to minimize an objective function.
        The variables (x) are continuous and represent the weight of each barrel to be used.
        Objective: The sum of x[i] should equal the target weight.
        Constraints: For each component (X, Y, Z, W, V), it sets up two constraints to ensure the sum of weighted percentages fall within a specified range, considering a 'fudge factor' of 2%.
        Solves the model and returns either a solution (list of weights and barrel numbers) or None.

    generate_targets():
        Generates random target mixtures based on provided ranges.
        Randomly picks a percentage for each component and normalizes them to sum up to 100%.
        Returns a list of Target objects.

    calculate_concentrations():
        Given a solution, it calculates the final composition of the mixture.
        Sums up the weighted percentages of each component (X, Y, Z, W, V) and divides by total weight to get the final percentages.

    main():
        Orchestrator function. Calls input_collector() to get initial data.
        Invokes generate_targets() to get a list of randomized targets.
        Loops through these targets, invokes find_solutions() to find viable solutions, and appends them to a list.
        Stops the loop after finding 10 viable solutions.
        Calls calculate_concentrations() to display the composition of each found solution.
        Finally, asks if the user wants to run the program again.

How It All Works Together:

    The main() function kicks things off by collecting inputs and generating random targets.
    It then iteratively calls find_solutions() for each target, keeping track of how many solutions it has found.
    For each solution, calculate_concentrations() is called to present the composition details.
    The user is asked if they'd like to try another set of inputs, looping back if the answer is 'yes'.

So, each function performs a specialized task, and main() stitches them together to solve the barrel mixing problem.