// AutoEthos Dashboard JavaScript

// Global variables
let socket;
let systemStatus = {};
let moderationHistory = [];
let analyticsData = {};

// Add at the top of the file (after global variables)
let moderationResultModalInstance = null;

// Initialize dashboard
document.addEventListener('DOMContentLoaded', function() {
    initializeSocket();
    initializeEventListeners();
    loadInitialData();
});

// Initialize WebSocket connection
function initializeSocket() {
    socket = io();
    
    socket.on('connect', function() {
        console.log('Connected to server');
        updateSystemStatus('Connected', 'connected');
    });
    
    socket.on('disconnect', function() {
        console.log('Disconnected from server');
        updateSystemStatus('Disconnected', 'disconnected');
    });
    
    socket.on('connected', function(data) {
        console.log('Dashboard connected:', data);
    });
    
    socket.on('system_status_update', function(data) {
        systemStatus = data;
        updateDashboardStats(data);
        updateAgentStatusGrid(data);
    });
    
    socket.on('history_update', function(data) {
        moderationHistory = data;
        updateRecentActivity(data);
    });
    
    socket.on('analytics_update', function(data) {
        analyticsData = data;
        updateDashboardStats(data);
    });
    
    socket.on('moderation_result', function(data) {
        showModerationResult(data);
    });
    
    socket.on('moderation_error', function(data) {
        showError(data.error);
    });
}

// Initialize event listeners
function initializeEventListeners() {
    // Quick moderation form
    const form = document.getElementById('quick-moderation-form');
    if (form) {
        form.addEventListener('submit', handleModerationSubmit);
    }
    
    // Real-time moderation via socket
    socket.on('request_moderation', function(data) {
        handleModerationRequest(data);
    });
}

// Load initial data
function loadInitialData() {
    // Load system status
    fetch('/api/system_status')
        .then(response => response.json())
        .then(data => {
            systemStatus = data;
            updateDashboardStats(data);
            updateAgentStatusGrid(data);
        })
        .catch(error => {
            console.error('Error loading system status:', error);
            updateSystemStatus('Error', 'disconnected');
        });
    
    // Load moderation history
    fetch('/api/moderation_history')
        .then(response => response.json())
        .then(data => {
            moderationHistory = data;
            updateRecentActivity(data);
        })
        .catch(error => {
            console.error('Error loading moderation history:', error);
        });
    
    // Load analytics
    fetch('/api/analytics')
        .then(response => response.json())
        .then(data => {
            analyticsData = data;
            updateDashboardStats(data);
        })
        .catch(error => {
            console.error('Error loading analytics:', error);
        });
}

// Handle moderation form submission
function handleModerationSubmit(event) {
    event.preventDefault();
    
    const content = document.getElementById('content-input').value.trim();
    if (!content) {
        showError('Please enter content to moderate');
        return;
    }
    
    const submitButton = document.getElementById('submit-moderation');
    const originalText = submitButton.innerHTML;
    
    // Show loading state
    submitButton.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Analyzing...';
    submitButton.disabled = true;
    
    // Prepare request data
    const requestData = {
        content: content,
        context: {
            content_type: document.getElementById('content-type').value,
            audience_size: parseInt(document.getElementById('audience-size').value),
            vulnerable_audience: document.getElementById('vulnerable-audience').checked,
            educational_value: document.getElementById('educational-value').checked,
            public_interest: document.getElementById('public-interest').checked,
            democratic_value: false,
            target_cultures: ['global'],
            audience_diversity: 'high'
        }
    };
    
    // Submit via API
    fetch('/api/submit_moderation', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            showError(data.error);
        } else {
            showModerationResult(data);
            // Clear form
            document.getElementById('content-input').value = '';
            document.getElementById('vulnerable-audience').checked = false;
            document.getElementById('educational-value').checked = false;
            document.getElementById('public-interest').checked = false;
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showError('Failed to submit moderation request');
    })
    .finally(() => {
        // Reset button
        submitButton.innerHTML = originalText;
        submitButton.disabled = false;
    });
}

// Handle moderation request via socket
function handleModerationRequest(data) {
    const content = data.content;
    const context = data.context || {};
    
    if (!content) {
        socket.emit('moderation_error', { error: 'Content is required' });
        return;
    }
    
    // Emit moderation request to server
    socket.emit('request_moderation', {
        content: content,
        context: context
    });
}

// Update system status indicator
function updateSystemStatus(status, type) {
    const indicator = document.getElementById('status-indicator');
    const statusText = document.getElementById('system-status');
    
    if (indicator && statusText) {
        indicator.className = `fas fa-circle text-${type} me-1 status-indicator ${type}`;
        statusText.textContent = status;
    }
}

// Update dashboard statistics
function updateDashboardStats(data) {
    // Update from analytics data
    if (data.total_decisions !== undefined) {
        document.getElementById('total-decisions').textContent = data.total_decisions;
    }
    
    if (data.average_confidence !== undefined) {
        const confidencePercent = Math.round(data.average_confidence * 100);
        document.getElementById('avg-confidence').textContent = `${confidencePercent}%`;
    }
    
    // Update from system status
    if (data.active_agents !== undefined) {
        document.getElementById('active-agents').textContent = data.active_agents;
    }
    
    if (data.total_agents !== undefined && data.active_agents !== undefined) {
        const consensusRate = data.total_agents > 0 ? Math.round((data.active_agents / data.total_agents) * 100) : 0;
        document.getElementById('consensus-rate').textContent = `${consensusRate}%`;
    }
}

// Update agent status grid
function updateAgentStatusGrid(data) {
    const grid = document.getElementById('agent-status-grid');
    if (!grid) return;
    
    if (!data.debate_agents) {
        grid.innerHTML = '<div class="col-12 text-center"><p class="text-muted">No agent data available</p></div>';
        return;
    }
    
    let html = '';
    
    // Add commander
    if (data.commander) {
        html += createAgentStatusCard('commander', data.commander);
    }
    
    // Add debate agents
    Object.entries(data.debate_agents).forEach(([name, agent]) => {
        html += createAgentStatusCard(name, agent);
    });
    
    grid.innerHTML = html;
}

// Create agent status card HTML
function createAgentStatusCard(name, agent) {
    const statusClass = agent.is_active ? 'active' : 'inactive';
    const statusIcon = agent.is_active ? 'fa-check-circle text-success' : 'fa-times-circle text-danger';
    
    return `
        <div class="col-md-6 col-lg-3">
            <div class="agent-status-card ${statusClass}">
                <div class="d-flex justify-content-between align-items-start mb-2">
                    <div>
                        <div class="agent-name">${agent.name}</div>
                        <div class="agent-framework">${agent.ethical_framework}</div>
                    </div>
                    <i class="fas ${statusIcon}"></i>
                </div>
                <div class="agent-metrics">
                    <div class="agent-metric">
                        <div class="agent-metric-value">${agent.response_count}</div>
                        <div class="agent-metric-label">Responses</div>
                    </div>
                    <div class="agent-metric">
                        <div class="agent-metric-value">${agent.queue_size}</div>
                        <div class="agent-metric-label">Queue</div>
                    </div>
                </div>
            </div>
        </div>
    `;
}

// Update recent activity feed
function updateRecentActivity(data) {
    const container = document.getElementById('recent-activity');
    if (!container) return;
    
    if (!data || data.length === 0) {
        container.innerHTML = '<div class="text-center text-muted"><p>No recent activity</p></div>';
        return;
    }
    
    // Take last 10 items
    const recentItems = data.slice(-10).reverse();
    
    let html = '';
    recentItems.forEach(item => {
        const decisionClass = getDecisionClass(item.final_decision);
        const timeAgo = formatTimeAgo(new Date(item.timestamp));
        
        html += `
            <div class="activity-item ${decisionClass}">
                <div class="activity-content text-truncate-2">${item.content_preview}</div>
                <div class="activity-decision">Decision: ${item.final_decision}</div>
                <div class="activity-time">${timeAgo} • ${item.agents_involved} agents</div>
            </div>
        `;
    });
    
    container.innerHTML = html;
}

// Get CSS class for decision type
function getDecisionClass(decision) {
    switch (decision.toLowerCase()) {
        case 'allow':
            return 'decision-allow';
        case 'remove':
            return 'decision-remove';
        case 'flag_for_review':
            return 'decision-flag';
        default:
            return '';
    }
}

// Format time ago
function formatTimeAgo(date) {
    const now = new Date();
    const diffMs = now - date;
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);
    
    if (diffMins < 1) return 'Just now';
    if (diffMins < 60) return `${diffMins}m ago`;
    if (diffHours < 24) return `${diffHours}h ago`;
    return `${diffDays}d ago`;
}

// Show moderation result modal
function showModerationResult(data) {
    try {
        const modalElement = document.getElementById('moderationResultModal');
        if (!modalElement) {
            console.error('Modal element not found');
            return;
        }
        // Create the modal instance only once
        if (!moderationResultModalInstance) {
            moderationResultModalInstance = new bootstrap.Modal(modalElement);
        }
        const content = document.getElementById('moderation-result-content');
        if (!content) {
            console.error('Modal content element not found');
            return;
        }
        const decisionClass = getDecisionClass(data.final_decision);
        const confidencePercent = Math.round((data.confidence || 0) * 100);
        let html = `
            <div class="row">
                <div class="col-12">
                    <div class="d-flex justify-content-between align-items-center mb-3">
                        <span class="decision-badge ${decisionClass}">${data.final_decision || 'UNKNOWN'}</span>
                        <span class="text-muted">Confidence: ${confidencePercent}%</span>
                    </div>
                    <div class="confidence-bar">
                        <div class="confidence-fill" style="width: ${confidencePercent}%"></div>
                    </div>
                </div>
            </div>
            <div class="row mt-3">
                <div class="col-12">
                    <h6>Reasoning:</h6>
                    <p class="text-muted">${data.reasoning || 'No reasoning provided'}</p>
                </div>
            </div>
        `;
        // Add individual agent responses
        if (data.individual_responses && Object.keys(data.individual_responses).length > 0) {
            html += '<div class="row mt-3"><div class="col-12"><h6>Agent Responses:</h6></div></div>';
            Object.entries(data.individual_responses).forEach(([name, response]) => {
                const responseDecisionClass = getDecisionClass(response.decision);
                const responseConfidence = Math.round((response.confidence || 0) * 100);
                html += `
                    <div class="agent-response-card">
                        <div class="agent-response-header">
                            <div>
                                <div class="agent-response-name">${response.agent_name || name}</div>
                                <div class="agent-response-framework">${response.ethical_framework || 'Unknown'}</div>
                            </div>
                            <span class="decision-badge ${responseDecisionClass}">${response.decision || 'UNKNOWN'}</span>
                        </div>
                        <div class="agent-response-decision">Confidence: ${responseConfidence}%</div>
                        <div class="agent-response-reasoning">${response.reasoning || 'No reasoning provided'}</div>
                        ${response.supporting_evidence && response.supporting_evidence.length > 0 ? `
                            <div class="agent-response-evidence">
                                <strong>Evidence:</strong><br>
                                ${response.supporting_evidence.map(evidence => 
                                    `<span class="evidence-item">${evidence}</span>`
                                ).join('')}
                            </div>
                        ` : ''}
                    </div>
                `;
            });
        }
        // Add deliberation summary
        if (data.deliberation_summary) {
            const summary = data.deliberation_summary;
            html += `
                <div class="row mt-3">
                    <div class="col-12">
                        <h6>Deliberation Summary:</h6>
                        <div class="row">
                            <div class="col-md-3">
                                <div class="text-center">
                                    <div class="h5 text-primary">${summary.agents_consulted || 0}</div>
                                    <small class="text-muted">Agents Consulted</small>
                                </div>
                            </div>
                            <div class="col-md-3">
                                <div class="text-center">
                                    <div class="h5 text-success">${summary.consensus_reached ? 'Yes' : 'No'}</div>
                                    <small class="text-muted">Consensus Reached</small>
                                </div>
                            </div>
                            <div class="col-md-3">
                                <div class="text-center">
                                    <div class="h5 text-warning">${summary.conflicts_resolved || 0}</div>
                                    <small class="text-muted">Conflicts Resolved</small>
                                </div>
                            </div>
                            <div class="col-md-3">
                                <div class="text-center">
                                    <div class="h5 text-info">${summary.deliberation_quality || 'Unknown'}</div>
                                    <small class="text-muted">Quality</small>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            `;
        }
        content.innerHTML = html;
        moderationResultModalInstance.show();
    } catch (error) {
        console.error('Error showing moderation result:', error);
        showError('Failed to display moderation result');
    }
}

// Show error message
function showError(message) {
    // Create toast notification
    const toastContainer = document.getElementById('toast-container') || createToastContainer();
    
    const toast = document.createElement('div');
    toast.className = 'toast align-items-center text-white bg-danger border-0';
    toast.setAttribute('role', 'alert');
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">
                <i class="fas fa-exclamation-triangle me-2"></i>
                ${message}
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;
    
    toastContainer.appendChild(toast);
    
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();
    
    // Remove toast after it's hidden
    toast.addEventListener('hidden.bs.toast', () => {
        toast.remove();
    });
}

// Create toast container if it doesn't exist
function createToastContainer() {
    const container = document.createElement('div');
    container.id = 'toast-container';
    container.className = 'toast-container position-fixed top-0 end-0 p-3';
    container.style.zIndex = '1055';
    document.body.appendChild(container);
    return container;
}

// Utility function to debounce API calls
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Auto-refresh data every 30 seconds
setInterval(() => {
    if (socket.connected) {
        socket.emit('request_update');
    }
}, 30000); 