from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from database import DATABASE_PATH

# Set up Flask application
app = Flask(__name__)
CORS(app)  # Allow CORS so that the frontend can interact with the backend

# Flask route to search for mice
@app.route('/search', methods=['POST'])
def search_mice():
    # Get search criteria from the request
    data = request.get_json()
    hand_length = data.get('hand_length')
    hand_width = data.get('hand_width')
    grip_type = data.get('grip_type')
    shape = data.get('shape')
    connection = data.get('connection')
    weight = data.get('weight')  # Max acceptable weight
    side_buttons = data.get('side_buttons')  # Number of side buttons
    leniency = data.get('leniency', 'medium')  # Default to medium leniency

    # Calculate target mouse dimensions based on user's hand size
    target_length = hand_length * 0.6
    target_width = hand_width * 0.6

    # Correction factors for different shapes
    correction_factors = {
        'Ergonomic': 0.86,
        'Symmetrical': 0.91
    }

    # Set leniency ranges (in cm) for length and width with adjusted proportional values
    leniency_ranges = {
        'high': {'length': 1.5, 'width': 0.9},   # Width is 60% of length
        'medium': {'length': 1.0, 'width': 0.6},  # Width is 60% of length
        'low': {'length': 0.5, 'width': 0.3}      # Width is 60% of length
    }
    leniency_range = leniency_ranges.get(leniency, {'length': 1.0, 'width': 0.6})

    # Connect to the database
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row  # Allow accessing rows as dictionaries
    cursor = conn.cursor()

    # Build the query dynamically based on provided criteria
    query = "SELECT * FROM mice WHERE 1=1"
    args = []
    if grip_type:
        query += " AND grip_type LIKE ?"
        args.append(f'%{grip_type}%')
    if shape:
        query += " AND shape LIKE ?"
        args.append(f'%{shape}%')
    if connection:
        query += " AND connectivity LIKE ?"
        args.append(f'%{connection}%')

    # Handle weight range filtering for '<50' and '100+'
    if weight:
        if weight == 50:  # '<50' case, filter for mice <= 50g
            query += " AND weight <= ?"
            args.append(50)
        elif weight == 100:  # '100+' case, filter for mice >= 100g
            query += " AND weight >= ?"
            args.append(100)
        else:
            query += " AND weight <= ?"
            args.append(weight)

    # Handle side buttons filtering
    if side_buttons is not None and side_buttons != "":
        query += " AND side_buttons = ?"
        args.append(side_buttons)

    # Execute query and fetch results
    mice = cursor.execute(query, args).fetchall()
    conn.close()

    # Filter results based on calculated target dimensions and leniency
    filtered_results = []
    for mouse in mice:
        mouse_shape = mouse['shape']
        correction_factor = correction_factors.get(mouse_shape, 1.0)
        adjusted_width = mouse['width'] * correction_factor

        # Check if mouse dimensions are within the leniency range for length and width
        if (target_length - leniency_range['length'] <= mouse['length'] <= target_length + leniency_range['length'] and
                target_width - leniency_range['width'] <= adjusted_width <= target_width + leniency_range['width']):
            filtered_results.append(dict(mouse))

    # Return filtered results as JSON
    return jsonify(filtered_results)

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
