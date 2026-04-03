async function sendCommand() {
    const cmd = document.getElementById('command').value;
    if (!cmd) return;

    try {
        const response = await fetch(`/send_command?cmd=${encodeURIComponent(cmd)}`);
        const data = await response.json();

        if (data.response) {
            document.getElementById('response').textContent = data.response;
        } else if (data.error) {
            document.getElementById('response').textContent = "Error: " + data.error;
        }
    } catch (err) {
        document.getElementById('response').textContent = "Request failed: " + err;
    }
}