"""
HSN Validator Web Application

This Flask application provides a web interface for the HSN Validator Agent.
"""

from flask import Flask, render_template, request, jsonify
import os
import json
from agent import (
    load_hsn_data,
    validate_hsn_code,
    validate_hsn_codes,
    process_hsn_validation_request
)
from create_sample_data import create_sample_data

# Initialize Flask app
app = Flask(__name__)

# Global data store
hsn_data_loaded = False

def ensure_data_loaded():
    """Ensure HSN data is loaded before processing requests"""
    global hsn_data_loaded
    
    if not hsn_data_loaded:
        # Create sample data if it doesn't exist
        if not os.path.exists("HSN_Master_Data.xlsx"):
            create_sample_data()
        
        # Load HSN data
        load_hsn_data("HSN_Master_Data.xlsx")
        hsn_data_loaded = True
        return {"status": "success", "message": "HSN data loaded successfully"}
    
    return {"status": "success", "message": "HSN data already loaded"}


@app.route('/')
def index():
    """Render the main page"""
    ensure_data_loaded()
    return render_template('index.html')


@app.route('/validate', methods=['POST'])
def validate():
    """API endpoint to validate HSN codes"""
    ensure_data_loaded()
    
    data = request.get_json()
    
    if not data:
        return jsonify({"status": "error", "message": "No data provided"})
    
    # Process single code
    if 'code' in data:
        code = data['code'].strip()
        if not code:
            return jsonify({"status": "error", "message": "HSN code is empty"})
        
        result = validate_hsn_code(code)
        return jsonify({
            "status": "success",
            "results": [result],
            "summary": {
                "total": 1,
                "valid": 1 if result.get("valid", False) else 0,
                "invalid": 0 if result.get("valid", False) else 1
            }
        })
    
    # Process multiple codes
    elif 'codes' in data:
        codes = data['codes']
        
        # Handle comma-separated string
        if isinstance(codes, str):
            codes = [code.strip() for code in codes.split(',') if code.strip()]
        
        if not codes:
            return jsonify({"status": "error", "message": "No HSN codes provided"})
        
        results = validate_hsn_codes(codes)
        return jsonify(results)
    
    return jsonify({"status": "error", "message": "Invalid request format"})


@app.route('/reload_data', methods=['POST'])
def reload_data():
    """API endpoint to reload HSN data"""
    global hsn_data_loaded
    
    # Reset the data loaded flag
    hsn_data_loaded = False
    
    # Reload the data
    result = ensure_data_loaded()
    
    return jsonify(result)


if __name__ == '__main__':
    # Ensure data is loaded on startup
    ensure_data_loaded()
    
    # Run the Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)
