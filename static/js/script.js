// JS: Logic to talk to your Flask app
async function sendCommand(customCmd = null) {
    const input = document.getElementById('cmdInput');
    const output = document.getElementById('console-output');

    // Use the button command if provided, otherwise grab from text box
    const command = customCmd || input.value;

    if (!command) return;

    // Show what we sent in the console
    output.innerHTML += `\n<span style="color: #aaa;">> ${command}</span>`;

    try {
        // This calls your Flask @app.route("/send_command")
        const response = await fetch(`/send_command?cmd=${encodeURIComponent(command)}`);
        const data = await response.json();

        if (data.response) {
            if (data.response.startsWith("Error:")) {
                output.innerHTML += `\n<span style="color: #ff4444;">${data.response}</span>`;
            } else {
                output.innerHTML += `\n${data.response}`;
            }
        } else if (data.error) {
            output.innerHTML += `\n<span style="color: red;">Error: ${data.error}</span>`;
        }
    } catch (err) {
        output.innerHTML += `\n<span style="color: red;">Network Error: Could not reach Flask server.</span>`;
    }

    // Auto-scroll to the bottom
    output.scrollTop = output.scrollHeight;

    // Clear input if it was a manual command
    if (!customCmd) input.value = '';
}

function runPreset(cmd) {
    sendCommand(cmd);
}

async function updateLiveStats() {

    const connectionBox = document.getElementById('connection-status'); // The Wrapper
    const navText = document.getElementById('nav-text'); // The specific text span
     // 3 things in older box
    //const mapLabel = document.getElementById('map-name');
    const playerLabel = document.getElementById('player-count');

    try {
        const response = await fetch(`/send_command?cmd=status`);

        // If the fetch fails or server returns error
        //if (!response.ok) throw new Error("Server Unreachable");

        const data = await response.json();

        if (data.response) {
            const raw = data.response;

            if (raw.startsWith("Error:")) {
                connectionBox.className = "status-indicator offline";
                navText.innerText = "SERVER DISCONNECTED";
                //navText.style.color = "red";
                //mapLabel.innerText = "---";
                playerLabel.innerText = "0/0";
                return;
            }
            else {
                connectionBox.className = "status-indicator online";
                navText.innerText = "SERVER CONNECTED";
                navText.style.color = "#00ff00";
            /*
            // 2. CS2 Map Parsing (Looking for the spawngroup pattern)
            // Pattern: SV: [1: de_inferno |
                const mapMatch = raw.match(/SV:\s*\[\d+:\s*([^\|\s\]]+)/i);
                if (mapMatch && mapMatch[1]) {
                    // This will strip "maps/prefabs/" if it exists and just show the name
                    let mapName = mapMatch[1].split('/').pop();
                    mapLabel.innerText = mapName;
                }

            // 3. Player Parsing (Looking for "0 humans, 2 bots")
                const humansMatch = raw.match(/(\d+)\s*humans/i);
                const botsMatch = raw.match(/(\d+)\s*bots/i);

                if (humansMatch && botsMatch) {
                    const total = parseInt(humansMatch[1]) + parseInt(botsMatch[1]);
                    playerLabel.innerText = `${total} (${humansMatch[1]}H / ${botsMatch[1]}B)`;
                }
                    */
            }
        }
    } catch (err) {
        // If fetch fails or rcon connection is dead
            connectionBox.className = "status-indicator offline";
            navText.innerText = "SERVER DISCONNECTED";
            navText.style.color = "red";
            //mapLabel.innerText = "---";
            //playerLabel.innerText = "0/0";
    }
}

function buildAndLaunch() {
    const map = document.getElementById('launchMap').value;
    const modeValue = document.getElementById('launchMode').value;
    
    if (!map) {
        alert("Please select a map first!");
        return;
    }

    if (!modeValue) {
        alert("Please select a game mode first!");
        return;
    }

    // Split the "0,1" into type=0 and mode=1
    const [type, mode] = modeValue.split(',');

    // Construct the command: Change settings FIRST, then load the map
    // We use semicolons (;) to send multiple commands at once
    const finalCmd = `game_type ${type}; game_mode ${mode}; map ${map}`;
    
    console.log("Executing Launch:", finalCmd);
    
    // Use your existing send function
    runPreset(finalCmd);

    document.getElementById('launchMap').selectedIndex = 0;
    document.getElementById('launchMode').selectedIndex = 0;
}

// Update stats every 10 seconds
setInterval(updateLiveStats, 10000);
// Run once on page load
updateLiveStats();