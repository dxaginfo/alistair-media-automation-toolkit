#!/usr/bin/env python3
"""
API module for SceneValidator to enable integration with other tools.
"""

import json
import logging
import os
from flask import Flask, request, jsonify
from validator import SceneValidator

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("scene_validator_api")

app = Flask(__name__)
validator = SceneValidator()

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint.
    
    Returns:
        JSON response with service status
    """
    return jsonify({
        "status": "healthy",
        "service": "SceneValidator API",
        "version": "1.0.0"
    })

@app.route('/validate/scene', methods=['POST'])
def validate_scene():
    """Validate a single scene.
    
    Expects JSON scene data in request body.
    
    Returns:
        JSON response with validation results
    """
    try:
        scene_data = request.json
        if not scene_data:
            return jsonify({"error": "No scene data provided"}), 400
        
        results = validator.validate_scene(scene_data)
        return jsonify(results)
    except Exception as e:
        logger.error(f"Error validating scene: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/validate/project', methods=['POST'])
def validate_project():
    """Validate a project (multiple scenes).
    
    Expects JSON array of scene data in request body.
    
    Returns:
        JSON response with validation results
    """
    try:
        project_data = request.json
        if not project_data or not isinstance(project_data, list):
            return jsonify({"error": "Invalid project data. Expected array of scenes"}), 400
        
        results = validator.validate_project(project_data)
        return jsonify(results)
    except Exception as e:
        logger.error(f"Error validating project: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/config', methods=['GET'])
def get_config():
    """Get current configuration.
    
    Returns:
        JSON response with current configuration
    """
    # Filter out sensitive information
    safe_config = {k: v for k, v in validator.config.items() if k not in ['api_key']}
    return jsonify(safe_config)

@app.route('/validation-rules', methods=['GET'])
def get_validation_rules():
    """Get current validation rules.
    
    Returns:
        JSON response with current validation rules
    """
    return jsonify(validator.validation_rules)

@app.route('/report-formats', methods=['GET'])
def get_report_formats():
    """Get available report formats.
    
    Returns:
        JSON response with available report formats
    """
    return jsonify({
        "available_formats": ["html", "json"],
        "default_format": validator.config.get("report_format", "html")
    })

def start_api(host='0.0.0.0', port=5000, debug=False):
    """Start the API server.
    
    Args:
        host: Host to bind to
        port: Port to bind to
        debug: Whether to run in debug mode
    """
    app.run(host=host, port=port, debug=debug)

if __name__ == '__main__':
    # Get port from environment or use default
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    logger.info(f"Starting SceneValidator API on port {port}, debug={debug}")
    start_api(port=port, debug=debug)