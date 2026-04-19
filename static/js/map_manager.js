function submitMap() {
    const id = document.getElementById('wsInput').value;
    
    if (!id) {
        alert("Please enter a Workshop ID first!");
        return;
    }

    fetch('/add_workshop_map', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ workshop_id: id })
    })
    .then(res => res.json())
    .then(data => {
        if(data.success) {
            alert("Added: " + data.map_name);
            location.reload();
        } else {
            alert("Error: " + data.error);
        }
    });
}