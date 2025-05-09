from flask import Flask, render_template, jsonify
from src.map_generator import generate_research_map

app = Flask(__name__)

@app.route('/')
def index():
    """Render the homepage with the research funding map"""
    return render_template('index.html')

@app.route('/map')
def map():
    """Generate and return the map HTML"""
    map_html = generate_research_map()
    return map_html

@app.route('/about')
def about():
    """Render the about page with project information"""
    return render_template('about.html')

@app.route('/api/universities')
def get_universities():
    """API endpoint to get university data in JSON format"""
    from src.data_loader import load_university_data
    universities = load_university_data()
    return jsonify(universities.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)
