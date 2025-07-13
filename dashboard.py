"""
EthIQ Web Dashboard
Flask-based web interface for the EthIQ ethical deliberation system
"""

import os
import json
import logging
import requests
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit, disconnect
import threading
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'ethiq-secret-key-2025'

# Initialize SocketIO with proper configuration
socketio = SocketIO(app, 
                   cors_allowed_origins="*",
                   async_mode='threading',
                   logger=True,
                   engineio_logger=True)

# Configuration
API_BASE_URL = "http://localhost:8000"
DASHBOARD_PORT = 8080

def check_api_health():
    """Check if the API server is running"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

def fetch_system_status():
    """Fetch system status from API"""
    try:
        response = requests.get(f"{API_BASE_URL}/api/agents", timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": "Failed to fetch system status"}
    except requests.exceptions.RequestException as e:
        return {"error": f"API connection error: {str(e)}"}

def fetch_moderation_history():
    """Fetch moderation history from API"""
    try:
        response = requests.get(f"{API_BASE_URL}/api/history", timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            return []
    except requests.exceptions.RequestException:
        return []

def fetch_analytics():
    """Fetch analytics data from API"""
    try:
        response = requests.get(f"{API_BASE_URL}/api/analytics/summary", timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": "Failed to fetch analytics"}
    except requests.exceptions.RequestException as e:
        return {"error": f"API connection error: {str(e)}"}

def background_updater():
    """Background task to update dashboard data"""
    while True:
        try:
            # Emit system status updates
            status = fetch_system_status()
            socketio.emit('system_status_update', status)
            
            # Emit analytics updates
            analytics = fetch_analytics()
            socketio.emit('analytics_update', analytics)
            
            time.sleep(10)  # Update every 10 seconds
        except Exception as e:
            logger.error(f"Background updater error: {e}")
            time.sleep(30)  # Wait longer on error

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
    """Agent management page"""
    return render_template('dashboard.html')

@app.route('/analytics')
def analytics_page():
    """Analytics page"""
    return render_template('dashboard.html')

@app.route('/history')
def history_page():
    """History page"""
    return render_template('dashboard.html')

@app.route('/integrations')
def integrations_page():
    """Integrations page"""
    return render_template('integrations.html')

@app.route('/api/submit_moderation', methods=['POST'])
def submit_moderation():
    """Submit content for moderation"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or 'content' not in data:
            return jsonify({"error": "Content is required"}), 400
        
        # Prepare request for API
        api_request = {
            "content": data.get('content', ''),
            "content_type": data.get('content_type', 'text'),
            "platform": data.get('platform', 'general'),
            "audience_size": data.get('audience_size', 1000),
            "vulnerable_audience": data.get('vulnerable_audience', False),
            "educational_value": data.get('educational_value', False),
            "public_interest": data.get('public_interest', False),
            "context": {
                "platform": data.get('platform', 'general'),
                "audience_size": data.get('audience_size', 1000),
                "vulnerable_audience": data.get('vulnerable_audience', False),
                "educational_value": data.get('educational_value', False),
                "public_interest": data.get('public_interest', False),
                "audience_diversity": data.get('audience_diversity', 'high')
            }
        }
        
        # Submit to API
        response = requests.post(
            f"{API_BASE_URL}/api/moderate",
            json=api_request,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            
            # Emit real-time update via WebSocket
            socketio.emit('moderation_complete', {
                'task_id': result.get('task_id'),
                'decision': result.get('final_decision'),
                'confidence': result.get('confidence'),
                'timestamp': datetime.now().isoformat()
            })
            
            return jsonify(result)
        else:
            return jsonify({"error": "API request failed"}), response.status_code
            
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"API connection error: {str(e)}"}), 503
    except Exception as e:
        logger.error(f"Moderation error: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/system_status')
def get_system_status():
    """Get system status"""
    return jsonify(fetch_system_status())

@app.route('/api/moderation_history')
def get_moderation_history():
    """Get moderation history"""
    return jsonify(fetch_moderation_history())

@app.route('/api/analytics')
def get_analytics():
    """Get analytics data"""
    return jsonify(fetch_analytics())

@app.route('/api/integrations/status')
def get_integrations_status():
    """Get integrations status"""
    try:
        # Check AgentOS integration
        agentos_response = requests.get(f"{API_BASE_URL}/api/integrations/agentos/status", timeout=5)
        agentos_status = agentos_response.json() if agentos_response.status_code == 200 else {"error": "Not available"}
        
        # Check Cloudera integration
        cloudera_response = requests.get(f"{API_BASE_URL}/api/integrations/cloudera/status", timeout=5)
        cloudera_status = cloudera_response.json() if cloudera_response.status_code == 200 else {"error": "Not available"}
        
        return jsonify({
            "agentos": agentos_status,
            "cloudera": cloudera_status,
            "timestamp": datetime.now().isoformat()
        })
    except requests.exceptions.RequestException as e:
        return jsonify({
            "agentos": {"error": f"Connection error: {str(e)}"},
            "cloudera": {"error": f"Connection error: {str(e)}"},
            "timestamp": datetime.now().isoformat()
        })

@app.route('/api/cloudera/analytics')
def get_cloudera_analytics():
    """Get Cloudera analytics"""
    try:
        response = requests.get(f"{API_BASE_URL}/api/integrations/cloudera/analytics", timeout=5)
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({"error": "Failed to fetch Cloudera analytics"})
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"API connection error: {str(e)}"})

@app.route('/api/submit_moderation_agentos', methods=['POST'])
def submit_moderation_agentos():
    """Submit content for moderation using AgentOS protocol"""
    try:
        data = request.get_json()
        
        if not data or 'content' not in data:
            return jsonify({"error": "Content is required"}), 400
        
        # Prepare request for AgentOS API
        api_request = {
            "content": data.get('content', ''),
            "content_type": data.get('content_type', 'text'),
            "platform": data.get('platform', 'general'),
            "audience_size": data.get('audience_size', 1000),
            "vulnerable_audience": data.get('vulnerable_audience', False),
            "educational_value": data.get('educational_value', False),
            "public_interest": data.get('public_interest', False),
            "context": {
                "platform": data.get('platform', 'general'),
                "audience_size": data.get('audience_size', 1000),
                "vulnerable_audience": data.get('vulnerable_audience', False),
                "educational_value": data.get('educational_value', False),
                "public_interest": data.get('public_interest', False),
                "audience_diversity": data.get('audience_diversity', 'high')
            }
        }
        
        # Submit to AgentOS API endpoint
        response = requests.post(
            f"{API_BASE_URL}/api/moderate/agentos",
            json=api_request,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            
            # Emit real-time update
            socketio.emit('agentos_moderation_complete', {
                'task_id': result.get('task_id'),
                'protocol': result.get('protocol'),
                'timestamp': datetime.now().isoformat()
            })
            
            return jsonify(result)
        else:
            return jsonify({"error": "AgentOS API request failed"}), response.status_code
            
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"API connection error: {str(e)}"}), 503
    except Exception as e:
        logger.error(f"AgentOS moderation error: {e}")
        return jsonify({"error": "Internal server error"}), 500

# WebSocket event handlers
@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    logger.info("Client connected")
    emit('connected', {'data': 'Connected to EthIQ Dashboard'})
    
    # Send initial data
    status = fetch_system_status()
    emit('system_status_update', status)
    
    analytics = fetch_analytics()
    emit('analytics_update', analytics)

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    logger.info("Client disconnected")

@socketio.on('request_moderation')
def handle_moderation_request(data):
    """Handle moderation request via WebSocket"""
    try:
        # Forward to API
        response = requests.post(
            f"{API_BASE_URL}/api/moderate",
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            emit('moderation_result', result)
        else:
            emit('moderation_error', {'error': 'API request failed'})
            
    except Exception as e:
        logger.error(f"WebSocket moderation error: {e}")
        emit('moderation_error', {'error': str(e)})

if __name__ == '__main__':
    # Start background updater in a separate thread
    updater_thread = threading.Thread(target=background_updater, daemon=True)
    updater_thread.start()
    
    # Check API health before starting
    if not check_api_health():
        print(f"⚠️  Warning: API server at {API_BASE_URL} is not responding")
        print("   The dashboard will work but some features may be limited")
        print("   Start the API server with: python start.py (option 3)")
        print()
    
    print(f"🌐 Starting EthIQ Dashboard on http://localhost:{DASHBOARD_PORT}")
    print("   Press Ctrl+C to stop")
    print()
    
    # Start the Flask-SocketIO server
    socketio.run(app, 
                host='0.0.0.0', 
                port=DASHBOARD_PORT, 
                debug=False,
                allow_unsafe_werkzeug=True)
