from flask import Flask, request, jsonify
import nfl_data_py as nfl

app = Flask(__name__)

# Data starts in 2016
START_YEAR = 2016

@app.route('/')
def index():
    return 'Welcome to your Flask application!'

@app.route('/getData', methods=['GET'])
def get_data():
    # Get parameters from the URL
    year = int(request.args.get('year'))
    week = int(request.args.get('week'))
    stat_type = request.args.get('type')

    # Check if the year is valid
    if year < START_YEAR:
        return jsonify({'error': 'Invalid year'})

    try:
        # Import the NGS data
        df = nfl.import_ngs_data(stat_type=stat_type)

        # Filter down to the specified week, season data
        df = df[(df['week'] == week) & (df['season'] == year)]
        df = df.reset_index()

        # Convert DataFrame to JSON
        result = df.to_json(orient='records')
        return result

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    # Configuration to allow access from any IP
    app.run(host='0.0.0.0', port=5000)
