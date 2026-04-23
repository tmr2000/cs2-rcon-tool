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

//Currently Unused - may be useful later
async function silentTransmit(command) {
    try {
        const response = await fetch(`/send_command?cmd=${encodeURIComponent(command)}`);
        return await response.json();
    } catch (err) {
        return { error: "Network Error" };
    }
}

async function updateLiveStats() {
    const connectionBox = document.getElementById('connection-status');
    const navText = document.getElementById('nav-text');

    try {
        const response = await fetch('/server_status');
        const data = await response.json();

        const serverEvent = new CustomEvent('serverUpdate', { detail: data });
        document.dispatchEvent(serverEvent);

        if (data && data.online) {
            connectionBox.className = "status-indicator online";
            navText.innerText = "SERVER CONNECTED";
            navText.style.color = "#00ff00";
        } 
        else {
            connectionBox.className = "status-indicator offline";
            navText.innerText = "SERVER DISCONNECTED";
            navText.style.color = "red";
        }
    } 
    catch (err) {
        connectionBox.className = "status-indicator offline";
        navText.innerText = "SERVER DISCONNECTED";
        navText.style.color = "red";
    }
}

updateLiveStats();
setInterval(() => {
    if (!document.hidden) {
        updateLiveStats();
    }
}, 5000);
document.addEventListener("visibilitychange", () => {
    if (!document.hidden) {
        updateLiveStats();
    }
});