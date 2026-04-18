// Console logic
async function sendCommand(customCmd = null) {
    const input = document.getElementById('cmdInput');
    const output = document.getElementById('console-output');
    const command = customCmd || (input ? input.value : null);

    if (!command || !output) return;

    output.innerHTML += `\n<span style="color: #aaa;">> ${command}</span>`;
    
    const data = await silentTransmit(command);

    if (data.response) {
        const color = data.response.startsWith("Error:") ? "#ff4444" : "inherit";
        output.innerHTML += `\n<span style="color: ${color};">${data.response}</span>`;
    }
    
    output.scrollTop = output.scrollHeight;
    if (!customCmd && input) input.value = '';
}

function runPreset(cmd) {
    sendCommand(cmd);
}

function buildAndLaunch() {
    const map = document.getElementById('launchMap').value;
    const modeValue = document.getElementById('launchMode').value;
    
    if (!map || !modeValue) {
        alert("Select map and mode!");
        return;
    }

    const [type, mode] = modeValue.split(',');
    runPreset(`game_type ${type}; game_mode ${mode}; map ${map}`);

    document.getElementById('launchMap').selectedIndex = 0;
    document.getElementById('launchMode').selectedIndex = 0;
    syncMapToMode();
}

// Clear button logic
const clearBtn = document.getElementById('clearBtn');
if (clearBtn) {
    clearBtn.addEventListener('click', () => {
        document.getElementById('console-output').innerHTML = '>';
    });
}

function syncMapToMode() {
    const modeSelect = document.getElementById('launchMode');
    const mapSelect = document.getElementById('launchMap');
    if (!modeSelect.value) {
        mapSelect.disabled = true;
        return;
    }
    mapSelect.disabled = false;
    const selectedType = modeSelect.options[modeSelect.selectedIndex].getAttribute('data-type');
    let currentMapStillValid = false;
    Array.from(mapSelect.options).forEach(opt => {
        if (opt.value === "") return; // Skip placeholder
        const attrVal = opt.getAttribute(`data-${selectedType}`);
        const isSupported = (attrVal === 'True' || attrVal === 'true' || attrVal === '1');
        if (isSupported) {
            opt.style.display = 'block';
            opt.disabled = false;
            if (opt.selected) currentMapStillValid = true;
        } else {
            opt.style.display = 'none';
            opt.disabled = true;
        }
    });
    if (!currentMapStillValid && mapSelect.selectedIndex !== 0) {
        mapSelect.selectedIndex = 0;
    }
}