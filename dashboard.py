#!/usr/bin/env python3
"""
EthIQ Dashboard - Web Interface for Ethical Deliberation System
Provides a modern web interface for content moderation and agent monitoring
"""

import asyncio
import json
import logging
import requests
import argparse
import sys
from datetime import datetime
from typing import Dict, Any, List

from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_socketio import SocketIO, emit
import threading
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Flask app configuration
app = Flask(__name__)
app.config['SECRET_KEY'] = 'ethiq-secret-key-2025'
socketio = SocketIO(app, cors_allowed_origins="*")

# API configuration
API_BASE_URL = "http://localhost:8000"
API_ENDPOINTS = {
    "health": f"{API_BASE_URL}/health",
    "moderate": f"{API_BASE_URL}/api/moderate",
    "agents": f"{API_BASE_URL}/api/agents",
    "history": f"{API_BASE_URL}/api/history",
    "analytics": f"{API_BASE_URL}/api/analytics/summary",
    "trends": f"{API_BASE_URL}/api/analytics/trends"
}

# Global state
system_status = {"status": "unknown", "agents": {}}
moderation_history = []
analytics_data = {}


def check_api_health():
    """Check if the API is running"""
    try:
        response = requests.get(API_ENDPOINTS["health"], timeout=5)
        return response.status_code == 200
    except:
        return False


def fetch_system_status():
    """Fetch current system status"""
    global system_status
    try:
        response = requests.get(API_ENDPOINTS["agents"], timeout=10)
        if response.status_code == 200:
            system_status = response.json()
            socketio.emit('system_status_update', system_status)
    except Exception as e:
        logger.error(f"Failed to fetch system status: {e}")


def fetch_moderation_history():
    """Fetch moderation history"""
    global moderation_history
    try:
        response = requests.get(API_ENDPOINTS["history"], timeout=10)
        if response.status_code == 200:
            moderation_history = response.json()
            socketio.emit('history_update', moderation_history)
    except Exception as e:
        logger.error(f"Failed to fetch moderation history: {e}")


def fetch_analytics():
    """Fetch analytics data"""
    global analytics_data
    try:
        response = requests.get(API_ENDPOINTS["analytics"], timeout=10)
        if response.status_code == 200:
            analytics_data = response.json()
            socketio.emit('analytics_update', analytics_data)
    except Exception as e:
        logger.error(f"Failed to fetch analytics: {e}")


def background_updater():
    """Background thread to update data periodically"""
    while True:
        if check_api_health():
            fetch_system_status()
            fetch_moderation_history()
            fetch_analytics()
        time.sleep(30)  # Update every 30 seconds


# Start background updater
updater_thread = threading.Thread(target=background_updater, daemon=True)
updater_thread.start()


@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('dashboard.html')


@app.route('/moderate')
def moderate_page():
    """Content moderation page"""
    return render_template('moderate.html')


@app.route('/agents')
def agents_page():
    """Agent monitoring page"""
    return render_template('agents.html')


@app.route('/analytics')
def analytics_page():
    """Analytics page"""
    return render_template('analytics.html')


@app.route('/history')
def history_page():
    """Moderation history page"""
    return render_template('history.html')


@app.route('/integrations')
def integrations_page():
    """Integrations page"""
    return render_template('integrations.html')


@app.route('/api/submit_moderation', methods=['POST'])
def submit_moderation():
    """Submit content for moderation"""
    try:
        data = request.json
        content = data.get('content', '')
        context = data.get('context', {})
        
        if not content:
            return jsonify({"error": "Content is required"}), 400
        
        # Prepare request for API
        moderation_request = {
            "content": content,
            "content_type": context.get('content_type', 'text'),
            "context": context,
            "platform": context.get('platform', 'general'),
            "audience_size": context.get('audience_size', 1000),
            "vulnerable_audience": context.get('vulnerable_audience', False),
            "educational_value": context.get('educational_value', False),
            "public_interest": context.get('public_interest', False),
            "democratic_value": context.get('democratic_value', False),
            "target_cultures": context.get('target_cultures', ['global']),
            "audience_diversity": context.get('audience_diversity', 'high')
        }
        
        # Submit to API
        response = requests.post(
            API_ENDPOINTS["moderate"],
            json=moderation_request,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            # Emit result to connected clients
            socketio.emit('moderation_result', result)
            return jsonify(result)
        else:
            return jsonify({"error": "Moderation failed"}), 500
            
    except Exception as e:
        logger.error(f"Error in submit_moderation: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/system_status')
def get_system_status():
    """Get current system status"""
    return jsonify(system_status)


@app.route('/api/moderation_history')
def get_moderation_history():
    """Get moderation history"""
    return jsonify(moderation_history)


@app.route('/api/analytics')
def get_analytics():
    """Get analytics data"""
    return jsonify(analytics_data)


@app.route('/api/integrations/status')
def get_integrations_status():
    """Get integrations status from API"""
    try:
        # Get AgentOS status
        agentos_response = requests.get(f"{API_BASE_URL}/api/integrations/agentos/status", timeout=5)
        agentos_status = agentos_response.json() if agentos_response.status_code == 200 else {"status": "error"}
        
        # Get Cloudera status
        cloudera_response = requests.get(f"{API_BASE_URL}/api/integrations/cloudera/status", timeout=5)
        cloudera_status = cloudera_response.json() if cloudera_response.status_code == 200 else {"status": "error"}
        
        return jsonify({
            "agentos": agentos_status,
            "cloudera": cloudera_status,
            "notion": {"status": "active", "integration": "Notion"}  # Already integrated
        })
    except Exception as e:
        return jsonify({"error": f"Integrations status failed: {str(e)}"})


@app.route('/api/cloudera/analytics')
def get_cloudera_analytics():
    """Get Cloudera analytics from API"""
    try:
        response = requests.get(f"{API_BASE_URL}/api/integrations/cloudera/analytics", timeout=10)
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({"error": "Failed to get Cloudera analytics"})
    except Exception as e:
        return jsonify({"error": f"Cloudera analytics failed: {str(e)}"})


@app.route('/api/submit_moderation_agentos', methods=['POST'])
def submit_moderation_agentos():
    """Submit content for moderation using GenAI AgentOS Protocol"""
    try:
        data = request.json
        content = data.get('content', '')
        context = data.get('context', {})
        
        if not content:
            return jsonify({"error": "Content is required"}), 400
        
        # Prepare request for API
        moderation_request = {
            "content": content,
            "content_type": context.get('content_type', 'text'),
            "context": context,
            "platform": context.get('platform', 'general'),
            "audience_size": context.get('audience_size', 1000),
            "vulnerable_audience": context.get('vulnerable_audience', False),
            "educational_value": context.get('educational_value', False),
            "public_interest": context.get('public_interest', False),
            "democratic_value": context.get('democratic_value', False),
            "target_cultures": context.get('target_cultures', ['global']),
            "audience_diversity": context.get('audience_diversity', 'high')
        }
        
        # Submit to AgentOS API endpoint
        response = requests.post(
            f"{API_BASE_URL}/api/moderate/agentos",
            json=moderation_request,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            # Emit result to connected clients
            socketio.emit('moderation_result_agentos', result)
            return jsonify(result)
        else:
            return jsonify({"error": "AgentOS moderation failed"}), 500
            
    except Exception as e:
        logger.error(f"Error in submit_moderation_agentos: {e}")
        return jsonify({"error": str(e)}), 500


@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    logger.info("Client connected")
    emit('connected', {'status': 'connected'})
    
    # Send current data
    emit('system_status_update', system_status)
    emit('history_update', moderation_history)
    emit('analytics_update', analytics_data)


@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    logger.info("Client disconnected")


@socketio.on('request_moderation')
def handle_moderation_request(data):
    """Handle moderation request from client"""
    try:
        content = data.get('content', '')
        context = data.get('context', {})
        
        if not content:
            emit('moderation_error', {'error': 'Content is required'})
            return
        
        # Submit moderation request
        moderation_request = {
            "content": content,
            "content_type": context.get('content_type', 'text'),
            "context": context,
            "platform": context.get('platform', 'general'),
            "audience_size": context.get('audience_size', 1000),
            "vulnerable_audience": context.get('vulnerable_audience', False),
            "educational_value": context.get('educational_value', False),
            "public_interest": context.get('public_interest', False),
            "democratic_value": context.get('democratic_value', False),
            "target_cultures": context.get('target_cultures', ['global']),
            "audience_diversity": context.get('audience_diversity', 'high')
        }
        
        response = requests.post(
            API_ENDPOINTS["moderate"],
            json=moderation_request,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            emit('moderation_result', result)
        else:
            emit('moderation_error', {'error': 'Moderation failed'})
            
    except Exception as e:
        logger.error(f"Error in handle_moderation_request: {e}")
        emit('moderation_error', {'error': str(e)})


if __name__ == '__main__':
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='EthIQ Dashboard')
    parser.add_argument('--port', type=int, default=8080, help='Port to run the dashboard on (default: 8080)')
    parser.add_argument('--host', type=str, default='0.0.0.0', help='Host to bind to (default: 0.0.0.0)')
    args = parser.parse_args()
    
    logger.info("Starting EthIQ Dashboard...")
    logger.info(f"API Base URL: {API_BASE_URL}")
    logger.info(f"Dashboard will run on {args.host}:{args.port}")
    
    # Check API health on startup
    if check_api_health():
        logger.info("API is running and healthy")
    else:
        logger.warning("API is not running. Please start the API server first.")
    
    # Run the dashboard
    try:
        socketio.run(app, host=args.host, port=args.port, debug=True)
    except OSError as e:
        if "Address already in use" in str(e):
            logger.error(f"Port {args.port} is already in use. Try a different port with --port")
            sys.exit(1)
        else:
            raise e
