function pollGameState() {
    fetch('/get_gsi_state')
        .then(res => res.json())
        .then(data => {
            if (!data || Object.keys(data).length === 0) return;

            // 1. Update Match Header
            if (data.map) {
                const mode = data.map.mode || 'Casual';
                const mapName = data.map.name ? data.map.name.replace('de_', '') : 'Unknown';
                document.getElementById('gameModeMap').innerText = `${mode} | ${mapName.toUpperCase()}`;
                
                // Update Team Scores if available
                if (data.map.team_ct) document.getElementById('ctScore').innerText = data.map.team_ct.score || 0;
                if (data.map.team_t) document.getElementById('tScore').innerText = data.map.team_t.score || 0;
            }

            // 2. Parse and Render Players
            if (data.allplayers) {
                const ctTable = document.getElementById('ctPlayerTable');
                const tTable = document.getElementById('tPlayerTable');
                
                ctTable.innerHTML = '';
                tTable.innerHTML = '';

                for (const [steamid, player] of Object.entries(data.allplayers)) {
                    const stats = player.match_stats || {};
                    const state = player.state || {};
                    
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${player.name || 'Unknown'}</td>
                        <td>$${state.money || 0}</td>
                        <td>${stats.kills || 0}</td>
                        <td>${stats.assists || 0}</td>
                        <td>${stats.deaths || 0}</td>
                        <td>${stats.score || 0}</td>
                    `;

                    if (player.team === 'CT') {
                        ctTable.appendChild(row);
                    } else if (player.team === 'T') {
                        tTable.appendChild(row);
                    }
                }
            }
        })
        .catch(err => console.error("Error polling GSI state:", err));
}

// Poll every 1 second
setInterval(pollGameState, 1000);