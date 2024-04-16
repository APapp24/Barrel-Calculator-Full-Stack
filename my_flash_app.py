from flask import Flask, request, jsonify, render_template
from Size_5_Barrel_Calculator_With_Range import Barrel, Target, find_solutions, generate_targets, calculate_concentrations
from flask_cors import CORS
import logging
from logging.handlers import RotatingFileHandler

import logging

logging.basicConfig(filename='app.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Configure logging
handler = RotatingFileHandler('server.log', maxBytes=10000000, backupCount=5)
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)

@app.route('/', methods=['GET'])
def index():
    app.logger.info("Rendering index page")
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    app.logger.info("Received request for calculation")
    data = request.json
    barrels_data = data['barrels']
    target_data = data['target']

    app.logger.debug(f"Barrels data: {barrels_data}")
    app.logger.debug(f"Target data: {target_data}")

    barrels = [Barrel(**barrel) for barrel in barrels_data]
    target = Target(**target_data)

    solutions = []
    targets = generate_targets(target.weight, target.x_range, target.y_range,
                               target.z_range, target.w_range, target.v_range)

    solution_count = 0
    for t in targets:
        if solution_count >= 10:
            break
        solution = find_solutions(barrels, t)
        if solution:
            concentrations = calculate_concentrations(solution, barrels)
            solutions.append((solution, t, concentrations))
            solution_count += 1

    if solutions:
        formatted_solutions = []
        for i, (solution, target, concentrations) in enumerate(solutions):
            formatted_solution = []
            formatted_solution.append(f"A solution has been found with the following composition: {concentrations}")
            formatted_solutions.append(formatted_solution)
            for weight, barrel_number in solution:
                if weight > 0:
                    formatted_solution.append(f"Take {round(weight, 2)} pounds from barrel {barrel_number}")
        app.logger.info(f"Calculation successful. Number of solutions found: {len(solutions)}")
        return jsonify({"Solution": formatted_solutions})
    else:
        app.logger.warning("Calculation completed but no solution found.")
        return jsonify({"Error": "No solution found."})

def calculate_concentrations(solution, barrels):
    # Your original function here, but return the string instead of printing it.
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

    return f"{percentage_x:.2f}% of X, {percentage_y:.2f}% of Y, {percentage_z:.2f}% of Z, {percentage_w:.2f}% of W, {percentage_v:.2f}% of V"

@app.errorhandler(500)
def internal_error(error):
    app.logger.error(f"Internal Server Error: {error}")
    return "Internal Server Error", 500

if __name__ == '__main__':
    app.logger.info("Starting Flask server")
    app.run(host='0.0.0.0', port=8000)
