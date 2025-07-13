// Dashboard JavaScript for EthIQ Ethical Deliberation System

let socket = null;
let updateInterval = null;

// Initialize dashboard
document.addEventListener('DOMContentLoaded', function() {
    initializeSocket();
    initializeEventListeners();
    startPeriodicUpdates();
});

// Socket.IO connection
function initializeSocket() {
    socket = io();
    
    socket.on('connect', function() {
        console.log('Connected to EthIQ dashboard');
        updateConnectionStatus(true);
    });
    
    socket.on('disconnect', function() {
        console.log('Disconnected from EthIQ dashboard');
        updateConnectionStatus(false);
    });
    
    socket.on('system_status_update', function(data) {
        updateSystemStatus(data);
    });
    
    socket.on('analytics_update', function(data) {
        updateAnalytics(data);
    });
    
    socket.on('deliberation_update', function(data) {
        updateDeliberationStatus(data);
    });
}

// Event listeners
function initializeEventListeners() {
    // Test moderation button
    const testButton = document.getElementById('test-moderation');
    if (testButton) {
        testButton.addEventListener('click', testModeration);
    }
    
    // Refresh button
    const refreshButton = document.getElementById('refresh-data');
    if (refreshButton) {
        refreshButton.addEventListener('click', refreshData);
    }
    
    // Settings form
    const settingsForm = document.getElementById('settings-form');
    if (settingsForm) {
        settingsForm.addEventListener('submit', saveSettings);
    }
}

// Update connection status
function updateConnectionStatus(connected) {
    const statusElement = document.getElementById('connection-status');
    if (statusElement) {
        statusElement.textContent = connected ? 'Connected' : 'Disconnected';
        statusElement.className = connected ? 'badge bg-success' : 'badge bg-danger';
    }
}

// Update system status
function updateSystemStatus(data) {
    // Update commander status
    if (data.commander) {
        updateAgentStatus('commander', data.commander);
    }
    
    // Update specialist agents
    if (data.debate_agents) {
        Object.keys(data.debate_agents).forEach(agentKey => {
            updateAgentStatus(agentKey, data.debate_agents[agentKey]);
        });
    }
    
    // Update system health
    const healthElement = document.getElementById('system-health');
    if (healthElement) {
        healthElement.textContent = data.system_health || 'Unknown';
        healthElement.className = `badge ${getHealthBadgeClass(data.system_health)}`;
    }
    
    // Update total agents
    const totalAgentsElement = document.getElementById('total-agents');
    if (totalAgentsElement) {
        totalAgentsElement.textContent = data.total_agents || 0;
    }
    
    // Update active agents
    const activeAgentsElement = document.getElementById('active-agents');
    if (activeAgentsElement) {
        activeAgentsElement.textContent = data.active_agents || 0;
    }
    
    // Update consensus rate
    const consensusRate = data.total_agents > 0 ? Math.round((data.active_agents / data.total_agents) * 100) : 0;
    document.getElementById('consensus-rate').textContent = `${consensusRate}%`;
}

// Update agent status
function updateAgentStatus(agentKey, agentData) {
    const agentElement = document.getElementById(`agent-${agentKey}`);
    if (!agentElement) return;
    
    // Update agent name
    const nameElement = agentElement.querySelector('.agent-name');
    if (nameElement) {
        nameElement.textContent = agentData.name || agentKey;
    }
    
    // Update status badge
    const statusElement = agentElement.querySelector('.agent-status');
    if (statusElement) {
        statusElement.textContent = agentData.is_active ? 'Active' : 'Inactive';
        statusElement.className = `badge ${agentData.is_active ? 'bg-success' : 'bg-danger'}`;
    }
    
    // Update framework
    const frameworkElement = agentElement.querySelector('.agent-framework');
    if (frameworkElement) {
        frameworkElement.textContent = agentData.ethical_framework || 'Unknown';
    }
    
    // Update response count
    const responseElement = agentElement.querySelector('.agent-responses');
    if (responseElement) {
        responseElement.textContent = agentData.response_count || 0;
    }
    
    // Update queue size
    const queueElement = agentElement.querySelector('.agent-queue');
    if (queueElement) {
        queueElement.textContent = agentData.queue_size || 0;
    }
}

// Update analytics
function updateAnalytics(data) {
    // Update total decisions
    const totalDecisionsElement = document.getElementById('total-decisions');
    if (totalDecisionsElement) {
        totalDecisionsElement.textContent = data.total_decisions || 0;
    }
    
    // Update decision distribution
    if (data.decision_distribution) {
        Object.keys(data.decision_distribution).forEach(decision => {
            const element = document.getElementById(`decision-${decision.toLowerCase()}`);
            if (element) {
                element.textContent = data.decision_distribution[decision] || 0;
            }
        });
    }
    
    // Update average confidence
    const avgConfidenceElement = document.getElementById('avg-confidence');
    if (avgConfidenceElement) {
        avgConfidenceElement.textContent = ((data.average_confidence || 0) * 100).toFixed(1) + '%';
    }
    
    // Update agent performance
    if (data.agent_performance) {
        Object.keys(data.agent_performance).forEach(agentKey => {
            const performance = data.agent_performance[agentKey];
            const element = document.getElementById(`performance-${agentKey}`);
            if (element) {
                element.textContent = performance.avg_confidence ? 
                    (performance.avg_confidence * 100).toFixed(1) + '%' : 'N/A';
            }
        });
    }
}

// Update deliberation status
function updateDeliberationStatus(data) {
    const statusElement = document.getElementById('deliberation-status');
    if (statusElement) {
        statusElement.textContent = data.status || 'Idle';
        statusElement.className = `badge ${getDeliberationBadgeClass(data.status)}`;
    }
    
    // Update progress bar
    const progressElement = document.getElementById('deliberation-progress');
    if (progressElement && data.progress !== undefined) {
        progressElement.style.width = `${data.progress}%`;
        progressElement.setAttribute('aria-valuenow', data.progress);
    }
}

// Test moderation
async function testModeration() {
    const testContent = document.getElementById('test-content').value;
    if (!testContent.trim()) {
        alert('Please enter test content');
        return;
    }
    
    try {
        const response = await fetch('/api/moderate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                content: testContent,
                context: {},
                user_id: 'test-user',
                platform: 'dashboard',
                audience_size: 1000,
                vulnerable_audience: false,
                educational_value: 0.5,
                public_interest: 0.5
            })
        });
        
        const result = await response.json();
        
        if (response.ok) {
            displayModerationResult(result);
        } else {
            alert('Moderation failed: ' + result.detail);
        }
    } catch (error) {
        console.error('Error testing moderation:', error);
        alert('Error testing moderation');
    }
}

// Display moderation result
function displayModerationResult(result) {
    const resultElement = document.getElementById('moderation-result');
    if (!resultElement) return;
    
    resultElement.innerHTML = `
        <div class="alert alert-${getDecisionAlertClass(result.decision)}">
            <h5>Decision: ${result.decision}</h5>
            <p><strong>Confidence:</strong> ${(result.confidence * 100).toFixed(1)}%</p>
            <p><strong>Reasoning:</strong> ${result.reasoning}</p>
            <p><strong>Task ID:</strong> ${result.task_id}</p>
        </div>
    `;
    
    resultElement.scrollIntoView({ behavior: 'smooth' });
}

// Refresh data
function refreshData() {
    fetchSystemStatus();
    fetchAnalytics();
}

// Fetch system status
async function fetchSystemStatus() {
    try {
        const response = await fetch('/api/agents');
        const data = await response.json();
        
        // Convert to expected format
        const statusData = {
            commander: {
                name: 'EthicsCommander',
                description: 'Master agent orchestrating ethical deliberation',
                ethical_framework: 'Multi-Framework Orchestration',
                is_active: true,
                queue_size: 0,
                response_count: 0
            },
            debate_agents: {},
            total_agents: data.length,
            active_agents: data.filter(agent => agent.is_active).length,
            system_health: 'healthy'
        };
        
        // Add specialist agents
        data.forEach(agent => {
            if (agent.name !== 'EthicsCommander') {
                const agentKey = agent.name.toLowerCase().replace('agent', '');
                statusData.debate_agents[agentKey] = agent;
            }
        });
        
        updateSystemStatus(statusData);
    } catch (error) {
        console.error('Error fetching system status:', error);
    }
}

// Fetch analytics
async function fetchAnalytics() {
    try {
        const response = await fetch('/api/analytics/summary');
        const data = await response.json();
        updateAnalytics(data);
    } catch (error) {
        console.error('Error fetching analytics:', error);
    }
}

// Save settings
function saveSettings(event) {
    event.preventDefault();
    
    const formData = new FormData(event.target);
    const settings = Object.fromEntries(formData.entries());
    
    // Save settings to localStorage
    localStorage.setItem('ethiq-settings', JSON.stringify(settings));
    
    alert('Settings saved successfully');
}

// Load settings
function loadSettings() {
    const settings = localStorage.getItem('ethiq-settings');
    if (settings) {
        const parsedSettings = JSON.parse(settings);
        
        Object.keys(parsedSettings).forEach(key => {
            const element = document.getElementById(key);
            if (element) {
                element.value = parsedSettings[key];
            }
        });
    }
}

// Start periodic updates
function startPeriodicUpdates() {
    updateInterval = setInterval(() => {
        fetchSystemStatus();
        fetchAnalytics();
    }, 5000); // Update every 5 seconds
}

// Stop periodic updates
function stopPeriodicUpdates() {
    if (updateInterval) {
        clearInterval(updateInterval);
        updateInterval = null;
    }
}

// Utility functions
function getHealthBadgeClass(health) {
    switch (health) {
        case 'healthy': return 'bg-success';
        case 'warning': return 'bg-warning';
        case 'critical': return 'bg-danger';
        default: return 'bg-secondary';
    }
}

function getDeliberationBadgeClass(status) {
    switch (status) {
        case 'active': return 'bg-primary';
        case 'completed': return 'bg-success';
        case 'failed': return 'bg-danger';
        default: return 'bg-secondary';
    }
}

function getDecisionAlertClass(decision) {
    switch (decision) {
        case 'ALLOW': return 'success';
        case 'REMOVE': return 'danger';
        case 'FLAG_FOR_REVIEW': return 'warning';
        default: return 'info';
    }
}

// Cleanup on page unload
window.addEventListener('beforeunload', function() {
    stopPeriodicUpdates();
    if (socket) {
        socket.disconnect();
    }
}); 