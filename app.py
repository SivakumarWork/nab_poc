#!/usr/bin/env python3
"""
NAB POC - Python Hello World Application
A simple Flask application for demonstrating Harness CI/CD pipeline
"""

from flask import Flask, jsonify
import os
import socket
from datetime import datetime

app = Flask(__name__)

# Configuration
VERSION = os.getenv('APP_VERSION', '1.0.0')
PORT = int(os.getenv('PORT', 8080))

@app.route('/')
def hello():
    """Main hello world endpoint"""
    return jsonify({
        'message': 'Hello World from NAB POC!',
        'version': VERSION,
        'hostname': socket.gethostname(),
        'timestamp': datetime.now().isoformat()
    })

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'version': VERSION
    }), 200

@app.route('/ready')
def ready():
    """Readiness check endpoint"""
    return jsonify({
        'status': 'ready',
        'version': VERSION
    }), 200

@app.route('/info')
def info():
    """Application information endpoint"""
    return jsonify({
        'application': 'NAB POC Python Hello World',
        'version': VERSION,
        'hostname': socket.gethostname(),
        'port': PORT,
        'environment': os.getenv('ENVIRONMENT', 'development'),
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    print(f"Starting NAB POC Hello World Application v{VERSION}")
    print(f"Listening on port {PORT}")
    app.run(host='0.0.0.0', port=PORT, debug=False)

