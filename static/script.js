document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('calcForm');
    const barrelNumberInput = document.getElementById('barrel_number');
    const barrelInputsDiv = document.getElementById('barrel_inputs');
    const resultDiv = document.getElementById('result');

    // Generate barrel input fields dynamically
    barrelNumberInput.addEventListener('change', function() {
        barrelInputsDiv.innerHTML = '';
        const numBarrels = parseInt(barrelNumberInput.value);
        for (let i = 1; i <= numBarrels; i++) {
            const fields = ['x_percent', 'y_percent', 'z_percent', 'w_percent', 'v_percent'];
            const barrelDiv = document.createElement('div');
            barrelDiv.innerHTML = `<strong>Barrel #${i}</strong><br>`;
            fields.forEach(field => {
                barrelDiv.innerHTML += `<label for="${field}_${i}">${field.toUpperCase()}:</label>
                                        <input type="number" id="${field}_${i}" name="${field}_${i}" required><br>`;
            });
            barrelInputsDiv.appendChild(barrelDiv);
        }
    });

    // Listen for form submission
    form.addEventListener('submit', function(event) {
        event.preventDefault();

        resultDiv.innerText = 'Calculating...'; // Loading message

        // Collect barrel data
        const barrels = [];
        const numBarrels = parseInt(barrelNumberInput.value);
        for (let i = 1; i <= numBarrels; i++) {
            const barrel = {};
            const fields = ['x_percent', 'y_percent', 'z_percent', 'w_percent', 'v_percent'];
            fields.forEach(field => {
                barrel[field] = parseFloat(document.getElementById(`${field}_${i}`).value);
            });
            barrel['number'] = i;
            barrels.push(barrel);
        }

        // Collect target data
        const target = {
            weight: parseFloat(document.getElementById('target_weight').value),
            x_range: [
                parseFloat(document.getElementById('target_x_min').value),
                parseFloat(document.getElementById('target_x_max').value)
            ],
            y_range: [
                parseFloat(document.getElementById('target_y_min').value),
                parseFloat(document.getElementById('target_y_max').value)
            ],
            z_range: [
                parseFloat(document.getElementById('target_z_min').value),
                parseFloat(document.getElementById('target_z_max').value)
            ],
            w_range: [
                parseFloat(document.getElementById('target_w_min').value),
                parseFloat(document.getElementById('target_w_max').value)
            ],
            v_range: [
                parseFloat(document.getElementById('target_v_min').value),
                parseFloat(document.getElementById('target_v_max').value)
            ]
        };

        const data = { barrels, target };

        // Make API request to Flask backend
        fetch('http://http://127.0.0.1:5000//calculate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        })
        .then(response => response.json())
        .then(data => {
            if (data['Solution']) {
                let formattedOutput = '';
                data['Solution'].forEach((solution, index) => {
                    formattedOutput += `Solution ${index + 1}:\n`;
                    solution.forEach(detail => {
                        formattedOutput += `${detail}\n`;
                    });
                    formattedOutput += '\n';
                });
                resultDiv.innerHTML = formattedOutput.replace(/\n/g, '<br>');
            } else {
                resultDiv.innerText = 'No solution found.';
            }
        })
        .catch(error => {
            console.error('Error:', error);
            resultDiv.innerText = 'An error occurred. Check console for details.';
        });
    });
});