// State management
const state = {
    isConnected: false,
    selectedTable: null,
    connectionDetails: null
};

// DOM Elements
const connectionForm = document.getElementById('connection-form');
const connectBtn = document.getElementById('connect-btn');
const connectionStatus = document.getElementById('connection-status');
const step1 = document.getElementById('step1');
const step2 = document.getElementById('step2');
const step3 = document.getElementById('step3');
const tablesContainer = document.getElementById('tables-container');
const backBtn1 = document.getElementById('back-btn-1');
const backBtn2 = document.getElementById('back-btn-2');
const newAnalysisBtn = document.getElementById('new-analysis-btn');
const analyticsInfo = document.getElementById('analytics-info');
const resultsBody = document.getElementById('results-body');

// Event Listeners
connectBtn.addEventListener('click', handleConnect);
backBtn1.addEventListener('click', () => goToStep(1));
backBtn2.addEventListener('click', () => goToStep(1));
newAnalysisBtn.addEventListener('click', () => goToStep(1));

// Reset form on load
window.addEventListener('load', () => {
    document.getElementById('port').value = '3306';
});

async function handleConnect() {
    const host = document.getElementById('host').value.trim();
    const port = document.getElementById('port').value.trim();
    const username = document.getElementById('username').value.trim();
    const password = document.getElementById('password').value;
    const schema = document.getElementById('schema').value.trim();

    // Validation
    if (!host || !port || !username || !password || !schema) {
        showStatus('Please fill in all fields', 'error');
        return;
    }

    connectBtn.disabled = true;
    connectBtn.textContent = 'Connecting...';
    showStatus('Connecting to database...', 'loading');

    try {
        const response = await fetch('/api/connect', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                host,
                port: parseInt(port),
                username,
                password,
                schema
            })
        });

        // Check if response is OK
        if (!response.ok) {
            const contentType = response.headers.get('content-type');
            let errorMsg = `HTTP Error ${response.status}`;
            
            if (contentType && contentType.includes('application/json')) {
                try {
                    const errorData = await response.json();
                    errorMsg = errorData.message || errorMsg;
                } catch (e) {
                    // Couldn't parse JSON, use HTTP status
                }
            } else {
                // Not JSON, try to get text
                try {
                    const text = await response.text();
                    if (text) errorMsg = text.substring(0, 200);
                } catch (e) {
                    // Couldn't read response
                }
            }
            throw new Error(errorMsg);
        }

        const contentType = response.headers.get('content-type');
        if (!contentType || !contentType.includes('application/json')) {
            throw new Error('Server returned invalid response format');
        }

        const data = await response.json();

        if (data.status === 'success') {
            state.isConnected = true;
            state.connectionDetails = { host, port, username, schema };
            showStatus('✓ Connected successfully!', 'success');
            connectBtn.textContent = 'Connect';
            connectBtn.disabled = false;
            
            // Load tables after a short delay
            setTimeout(() => loadTables(), 500);
        } else {
            throw new Error(data.message || 'Connection failed');
        }
    } catch (error) {
        showStatus(`✗ ${error.message}`, 'error');
        connectBtn.textContent = 'Connect';
        connectBtn.disabled = false;
    }
}

async function loadTables() {
    try {
        const response = await fetch('/api/tables');
        const data = await response.json();

        if (data.status === 'success' && data.tables.length > 0) {
            displayTables(data.tables);
            goToStep(2);
        } else {
            showStatus('No tables found in the database', 'error');
        }
    } catch (error) {
        showStatus(`Error loading tables: ${error.message}`, 'error');
    }
}

function displayTables(tables) {
    const grid = document.createElement('div');
    grid.className = 'tables-grid';

    tables.forEach(table => {
        const button = document.createElement('button');
        button.type = 'button';
        button.className = 'table-button';
        button.textContent = table;
        button.addEventListener('click', () => selectTable(table, button));
        grid.appendChild(button);
    });

    tablesContainer.innerHTML = '';
    tablesContainer.appendChild(grid);
}

function selectTable(tableName, buttonElement) {
    // Remove previous selection
    document.querySelectorAll('.table-button').forEach(btn => btn.classList.remove('selected'));
    
    // Select new table
    buttonElement.classList.add('selected');
    state.selectedTable = tableName;

    // Load analytics
    loadAnalytics(tableName);
}

async function loadAnalytics(tableName) {
    try {
        goToStep(3);
        analyticsInfo.innerHTML = `<div class="spinner"></div><p>Analyzing ${tableName}...</p>`;
        resultsBody.innerHTML = '';

        const response = await fetch('/api/analytics', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                table: tableName
            })
        });

        const data = await response.json();

        if (data.status === 'success') {
            displayAnalytics(data.data, tableName);
        } else {
            throw new Error(data.message || 'Analytics failed');
        }
    } catch (error) {
        analyticsInfo.innerHTML = `<p style="color: red;">✗ Error: ${error.message}</p>`;
    }
}

function displayAnalytics(results, tableName) {
    if (!results || results.length === 0) {
        analyticsInfo.innerHTML = `<p>No data available for analysis in ${tableName}</p>`;
        return;
    }

    analyticsInfo.innerHTML = `
        <p><strong>Table:</strong> ${tableName}</p>
        <p><strong>Total Customers Analyzed:</strong> ${results.length}</p>
        <p><strong>Analysis Date:</strong> ${new Date().toLocaleString()}</p>
    `;

    resultsBody.innerHTML = '';

    results.forEach(result => {
        const row = document.createElement('tr');
        const classificationClass = `status-${result.customer_classification.toLowerCase()}`;
        
        row.innerHTML = `
            <td>${escapeHtml(result.customer_id)}</td>
            <td>${result.total_orders}</td>
            <td>${result.avg_order_gap || 'N/A'}</td>
            <td>${result.last_order_date || 'N/A'}</td>
            <td>${result.predicted_next_order_date || 'N/A'}</td>
            <td><span class="status-badge ${classificationClass}">${result.customer_classification}</span></td>
        `;
        resultsBody.appendChild(row);
    });
}

function showStatus(message, type) {
    connectionStatus.textContent = message;
    connectionStatus.className = '';
    
    if (type === 'success') {
        connectionStatus.classList.add('success');
    } else if (type === 'error') {
        connectionStatus.classList.add('error');
    } else if (type === 'loading') {
        connectionStatus.innerHTML = `<div class="spinner"></div>${message}`;
    }
}

function goToStep(stepNumber) {
    step1.classList.toggle('hidden', stepNumber !== 1);
    step2.classList.toggle('hidden', stepNumber !== 2);
    step3.classList.toggle('hidden', stepNumber !== 3);

    // Clear status when leaving step 1
    if (stepNumber !== 1) {
        connectionStatus.innerHTML = '';
    }

    // Reset selection when going back to step 1
    if (stepNumber === 1) {
        state.selectedTable = null;
        document.querySelectorAll('.table-button').forEach(btn => btn.classList.remove('selected'));
    }
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
