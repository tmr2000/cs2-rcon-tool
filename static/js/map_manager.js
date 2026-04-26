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
                    <div class="card-actions">
                        <button class="workshop-btn" onclick="window.open('https://steamcommunity.com/sharedfiles/filedetails/?id=${map.id}', '_blank')">
                            <svg viewBox="0 0 512 512" width="12" height="12" fill="currentColor">
                                <path d="M352 0c-12.9 0-24.6 7.8-29.6 19.8s-2.2 25.7 6.9 34.9L370.7 96 201.4 265.4c-12.5 12.5-12.5 32.8 0 45.3s32.8 12.5 45.3 0L416 141.3l41.4 41.4c9.2 9.2 22.9 11.9 34.9 6.9s19.8-16.6 19.8-29.6V32c0-17.7-14.3-32-32-32H352zM80 32C35.8 32 0 67.8 0 112V432c0 44.2 35.8 80 80 80H400c44.2 0 80-35.8 80-80V320c0-17.7-14.3-32-32-32s-32 14.3-32 32V432c0 8.8-7.2 16-16 16H80c-8.8 0-16-7.2-16-16V112c0-8.8 7.2-16 16-16H192c17.7 0 32-14.3 32-32s-14.3-32-32-32H80z"/>
                            </svg>
                        </button>
                        <button class="edit-btn" onclick="editMapName('${map.id}', '${escapedName}')">
                            <svg viewBox="0 0 512 512" width="14" height="14" fill="currentColor">
                                <path d="M471.6 21.7c-21.9-21.9-57.3-21.9-79.2 0L362.3 51.7l97.9 97.9 30.1-30.1c21.9-21.9 21.9-57.3 0-79.2L471.6 21.7zm-299.2 220c-6.1 6.1-10.8 13.6-13.5 21.9l-29.6 88.8c-2.9 8.6-.6 18.1 5.8 24.6s15.9 8.7 24.6 5.8l88.8-29.6c8.2-2.7 15.7-7.4 21.9-13.5L437.7 172.3 339.7 74.3 172.4 241.7zM96 64C43 64 0 107 0 160V416c0 53 43 96 96 96H352c53 0 96-43 96-96V320c0-17.7-14.3-32-32-32s-32 14.3-32 32v96c0 17.7-14.3 32-32 32H96c-17.7 0-32-14.3-32-32V160c0-17.7 14.3-32 32-32h96c17.7 0 32-14.3 32-32s-14.3-32-32-32H96z"/>
                            </svg>
                        </button>
                        <button class="delete-btn" onclick="deleteMap('${map.id}')">
                            <svg viewBox="0 0 448 512" width="16" height="16" fill="currentColor">
                                <path d="M135.2 17.7C140.6 6.8 151.7 0 163.8 0H284.2c12.1 0 23.2 6.8 28.6 17.7L320 32h96c17.7 0 32 14.3 32 32s-14.3 32-32 32H32C14.3 96 0 81.7 0 64S14.3 32 32 32h96l7.2-14.3zM32 128H416V448c0 35.3-28.7 64-64 64H96c-35.3 0-64-28.7-64-64V128zm96 64c-8.8 0-16 7.2-16 16V432c0 8.8 7.2 16 16 16s16-7.2 16-16V208c0-8.8-7.2-16-16-16zm96 0c-8.8 0-16 7.2-16 16V432c0 8.8 7.2 16 16 16s16-7.2 16-16V208c0-8.8-7.2-16-16-16zm96 0c-8.8 0-16 7.2-16 16V432c0 8.8 7.2 16 16 16s16-7.2 16-16V208c0-8.8-7.2-16-16-16z"/>
                            </svg>
                        </button>
                    </div>
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
