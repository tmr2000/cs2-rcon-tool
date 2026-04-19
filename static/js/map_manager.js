function submitMap() {
    const status = document.getElementById('statusMessage');
    const btn = document.querySelector('.map-manager-card button');
    const id = document.getElementById('wsInput').value;
    
    if (!id) {
        status.innerHTML = "Error: Please enter a Workshop ID.";
        status.style.color = "#ff4444";
        return;
    }

    status.innerHTML = "Connecting to Steam... please wait.";
    status.style.color = "#ff7417"; 
    btn.disabled = true; 
    btn.innerText = "Adding...";

    fetch('/add_workshop_map', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ workshop_id: id })
    })
    .then(res => res.json())
    .then(data => {
        if(data.success) {
            status.innerHTML = `Success! Added ${data.map_name}. Reloading...`;
            status.style.color = "#44ff44"; // Green for success
            setTimeout(() => {
                location.reload();
            }, 1500);
        } else {
            status.innerHTML = "Error: " + data.error;
            status.style.color = "#ff4444";
            btn.disabled = false;
            btn.innerText = "Add Map";
        }
    });

}

function editMapName(mapId, currentName) {
    const newName = prompt("Enter a new display name for this map:", currentName);
    // Only proceed if they typed something and didn't hit cancel
    if (newName && newName.trim() !== "") {
        fetch(`/update_map_name/${mapId}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ new_name: newName.trim() })
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                loadWorkshopGrid(); // Refresh the UI to show the new name
            } else {
                alert("Update failed: " + data.error);
            }
        })
        .catch(err => console.error("Error updating name:", err));
    }
}

function loadWorkshopGrid() {
    fetch('/get_workshop_maps')
        .then(res => res.json())
        .then(maps => {
            const grid = document.getElementById('workshopGrid');
            grid.innerHTML = ''; // Clear existing

            maps.forEach(map => {
                let escapedName = map.name.replace(/'/g, "\\'");
                const card = document.createElement('div');
                card.className = 'map-card';
                // Inside your maps.forEach loop where you define 'card.innerHTML':
                card.innerHTML = `
                    <button class="edit-btn" onclick="editMapName('${map.id}', '${escapedName}')">
                        <svg viewBox="0 0 512 512" width="12" height="12" fill="currentColor">
                            <path d="M410.3 231l11.3-11.3-33.9-33.9-62.1-62.1L291.7 89.8l-11.3 11.3-22.6 22.6L58.6 322.9c-10.4 10.4-18 23.3-22.2 37.4L1 481.2C-1.5 489.7 .8 498.8 7 505s15.3 8.5 23.7 6.1l120.9-35.4c14.1-4.2 27-11.8 37.4-22.2L387.7 253.6 410.3 231zM160 399.4l-9.1 22.7c-4 3.1-8.5 5.4-13.3 6.9L59.4 452l23-78.1c1.4-4.9 3.8-9.4 6.9-13.3l22.7-9.1v32c0 8.8 7.2 16 16 16h32zM362.7 18.7L348.3 33.2 425.7 110.5l14.5-14.5c25-25 25-65.5 0-90.5L453.3 1.9c-25-25-65.5-25-90.5 0z"/>
                        </svg>
                    </button>
                    <button class="delete-btn" onclick="deleteMap('${map.id}')">
                        <svg viewBox="0 0 448 512" width="12" height="12" fill="currentColor">
                            <path d="M135.2 17.7L128 32H32C14.3 32 0 46.3 0 64S14.3 96 32 96H416c17.7 0 32-14.3 32-32s-14.3-64-32-64H320l-7.2-14.3C307.4 6.8 296.3 0 284.2 0H163.8c-12.1 0-23.2 6.8-28.6 17.7zM416 128H32L53.2 467c1.6 25.3 22.6 45 47.9 45H346.9c25.3 0 46.3-19.7 47.9-45L416 128z"/>
                        </svg>
                    </button>
                    <img src="${map.image}" alt="${escapedName}" onerror="this.src='/static/img/placeholder.jpg'">
                    <div class="map-info">
                        <span class="map-name">${escapedName}</span>
                        <span class="map-id">ID: ${map.id}</span>
                    </div>
                `;
                grid.appendChild(card);
            });
        });
}

// Run this when the page opens
document.addEventListener('DOMContentLoaded', loadWorkshopGrid);

function deleteMap(mapId) {
    // 1. Double check with the user
    if (!confirm(`Are you sure you want to remove map ${mapId}?`)) return;

    // 2. Send the request to the backend
    fetch(`/delete_workshop_map/${mapId}`, {
        method: 'DELETE',
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            // 3. Refresh the grid to show it's gone
            loadWorkshopGrid(); 
        } else {
            alert("Error deleting map: " + data.error);
        }
    })
    .catch(err => {
        console.error("Delete failed:", err);
        alert("Server error while deleting.");
    });
}
