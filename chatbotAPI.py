from flask import Flask, request, jsonify
import pandas as pd
from fuzzywuzzy import process

app = Flask(__name__)

# Load the dataset
df = pd.read_csv('Task.csv')

# Preprocess data (remove special characters, convert to lowercase)
df['Medicine_Name'] = df['Medicine_Name'].str.replace('[^\w\s]', '').str.lower()

# Create a dictionary mapping lowercase medicine names to descriptions
medicine_dict = dict(zip(df['Medicine_Name'], df['Description']))

# API endpoint to retrieve description based on medicine name
@app.route('/medicine', methods=['GET'])
def get_medicine_description():
    medicine_name = request.args.get('name', '').lower()  # Convert user input to lowercase

    # Use fuzzy matching to find the closest match to the input name
    matched_name, score = process.extractOne(medicine_name, medicine_dict.keys())

    # Retrieve description using the matched name
    description = medicine_dict.get(matched_name, 'Medicine not found.')

    return jsonify({'matched_name': matched_name, 'description': description, 'score': score})

if __name__ == '__main__':
    app.run(debug=True)
