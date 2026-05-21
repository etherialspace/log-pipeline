const API_URL = 'http://127.0.0.1:8000/logs/';
let logsCache = [];
let pollInterval;
let isAutoRefresh = true;

const tableBody = document.getElementById('logs-body');
const loadingState = document.getElementById('loading-state');
const totalLogsEl = document.getElementById('total-logs');
const errorLogsEl = document.getElementById('error-logs');
const servicesActiveEl = document.getElementById('services-active');
const refreshBtn = document.getElementById('refresh-btn');
const autoRefreshToggle = document.getElementById('auto-refresh-toggle');

// Format timestamp
function formatTime(isoString) {
    const date = new Date(isoString);
    return date.toLocaleTimeString([], { hour12: false, hour: '2-digit', minute:'2-digit', second:'2-digit' }) + '.' + date.getMilliseconds().toString().padStart(3, '0');
}

function getLevelClass(level) {
    return level.toLowerCase();
}

function renderRow(log, isNew = false) {
    const tr = document.createElement('tr');
    if (isNew) tr.classList.add('new-row');
    
    tr.innerHTML = `
        <td class="td-timestamp">${formatTime(log.timestamp)}</td>
        <td><span class="badge ${getLevelClass(log.level)}">${log.level}</span></td>
        <td class="td-service">${log.service}</td>
        <td class="td-trace">${log.trace_id}</td>
        <td class="td-latency">${log.latency_ms}ms</td>
        <td class="td-message" title="${log.message}">${log.message}</td>
    `;
    return tr;
}

function updateStats(logs) {
    totalLogsEl.textContent = logs.length.toLocaleString();
    errorLogsEl.textContent = logs.filter(l => l.level === 'ERROR').length.toLocaleString();
    const services = new Set(logs.map(l => l.service));
    servicesActiveEl.textContent = services.size;
}

async function fetchLogs(isInitial = false) {
    try {
        if (isInitial && logsCache.length === 0) {
            loadingState.classList.remove('hidden');
        }
        
        // Fetch up to 100 logs
        const response = await fetch(`${API_URL}?limit=100`);
        const logs = await response.json();
        
        // Sort descending
        logs.sort((a, b) => b.id - a.id);
        
        loadingState.classList.add('hidden');
        
        if (logs.length === 0) return;
        
        const newLogs = [];
        if (logsCache.length > 0) {
            const lastKnownId = logsCache[0].id;
            newLogs.push(...logs.filter(l => l.id > lastKnownId));
        } else {
            newLogs.push(...logs);
        }
        
        if (newLogs.length > 0) {
            if (isInitial || logsCache.length === 0) {
                tableBody.innerHTML = '';
                logs.forEach(log => tableBody.appendChild(renderRow(log)));
            } else {
                newLogs.reverse().forEach(log => {
                    tableBody.prepend(renderRow(log, true));
                });
            }
            logsCache = logs;
            updateStats(logs);
        }
        
    } catch (error) {
        console.error("Error fetching logs:", error);
        if (logsCache.length === 0) {
            loadingState.innerHTML = `<p style="color:var(--level-error)">Failed to connect to API</p>`;
        }
    }
}

function toggleAutoRefresh(e) {
    isAutoRefresh = e.target.checked;
    if (isAutoRefresh) {
        startPolling();
    } else {
        stopPolling();
    }
}

function startPolling() {
    if (pollInterval) clearInterval(pollInterval);
    pollInterval = setInterval(() => fetchLogs(false), 2000);
}

function stopPolling() {
    if (pollInterval) clearInterval(pollInterval);
}

// Event Listeners
refreshBtn.addEventListener('click', () => {
    const svg = refreshBtn.querySelector('svg');
    svg.style.transform = 'rotate(180deg)';
    svg.style.transition = 'transform 0.5s ease';
    setTimeout(() => {
        svg.style.transform = '';
        svg.style.transition = '';
    }, 500);
    fetchLogs(false);
});
autoRefreshToggle.addEventListener('change', toggleAutoRefresh);

// Init
fetchLogs(true);
startPolling();
