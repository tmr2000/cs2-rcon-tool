// Global RCON Sender - Accessible by all other scripts
async function transmitRcon(command) {
    if (!command) return null;
    try {
        const response = await fetch(`/send_command?cmd=${encodeURIComponent(command)}`);
        return await response.json();
    } catch (err) {
        console.error("Network Error:", err);
        return { error: "Could not reach server" };
    }
}

async function silentTransmit(command) {
    try {
        const response = await fetch(`/send_command?cmd=${encodeURIComponent(command)}`);
        return await response.json();
    } catch (err) {
        return { error: "Network Error" };
    }
}

// Global Status Updater
async function updateLiveStats() {
    const connectionBox = document.getElementById('connection-status');
    const navText = document.getElementById('nav-text');

    const data = await silentTransmit('status');

    if (data && data.response && !data.response.startsWith("Error:")) {
        connectionBox.className = "status-indicator online";
        navText.innerText = "SERVER CONNECTED";
        navText.style.color = "#00ff00";
        return data.response; // Return raw data in case other scripts want it
    } else {
        connectionBox.className = "status-indicator offline";
        navText.innerText = "SERVER DISCONNECTED";
        navText.style.color = "red";
        return null;
    }
}

// Start the heartbeat
setInterval(updateLiveStats, 5000);
updateLiveStats();