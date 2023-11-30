from flask import Flask, render_template, jsonify
import csv
import os
from glob import glob

app = Flask(__name__)

def find_latest_file(directory, file_extension=".csv"):
    """Find the latest file in the given directory with the specified file extension."""
    list_of_files = glob(f"{directory}/*{file_extension}")
    print(f"Found files: {list_of_files}")  # Debugging
    if not list_of_files:
        return None
    latest_file = max(list_of_files, key=os.path.getctime)
    print(f"Latest file: {latest_file}")  # Debugging
    return latest_file

def read_csv_file(filename):
    """Read data from a CSV file."""
    data = []
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)
    return data

@app.route('/')
def index():
    """Render the index page."""
    return render_template('index.html')

@app.route('/data')
def data():
    """Return the data of the latest CSV file in JSON format."""
    filename = find_latest_file('sessions')  # Finds the latest CSV file in 'sessions'
    if filename:
        return jsonify(read_csv_file(filename))
    else:
        print("No CSV file found in 'sessions' directory.")  # Debugging
        return jsonify([])  # Return empty list if no file found

if __name__ == '__main__':
    app.run(debug=True)
