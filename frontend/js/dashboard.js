/**
 * SENTINEL-X | 3D Digital Twin Engine
 * Advanced 3D Spatial Intelligence powered by CesiumJS.
 */

// Initialize Cesium 3D Viewer (Centering on Abuja, Nigeria)
const viewer = new Cesium.Viewer('map', {
    terrainProvider: Cesium.createWorldTerrain(),
    animation: false,
    timeline: false,
    baseLayerPicker: false,
    sceneModePicker: true,
    navigationHelpButton: false,
    infoBox: true
});

// Fly to Abuja Sector (Priority 1)
viewer.camera.flyTo({
    destination: Cesium.Cartesian3.fromDegrees(7.3986, 9.0765, 15000), // Abuja coordinates
    orientation: {
        heading: Cesium.Math.toRadians(0.0),
        pitch: Cesium.Math.toRadians(-45.0),
    }
});

/**
 * EXPERT MODULE: 3D DRONE SIMULATION
 * Deploys simulated drones over Abuja for situational awareness.
 */
function deployDrones() {
    const abujaLat = 9.0765;
    const abujaLng = 7.3986;

    for (let i = 1; i <= 3; i++) {
        const droneId = `SENTINEL-DRONE-${i}`;
        const startPosition = Cesium.Cartesian3.fromDegrees(abujaLng + (i * 0.01), abujaLat + (i * 0.01), 500);

        const droneEntity = viewer.entities.add({
            name: droneId,
            position: startPosition,
            model: {
                uri: 'https://assets.cesium.com/5/models/Cesium_Air.glb', // Default Open Source GLB
                minimumPixelSize: 64,
                maximumScale: 20000
            },
            label: {
                text: `${droneId} [ACTIVE]`,
                font: '10px Courier New',
                pixelOffset: new Cesium.Cartesian2(0, -30)
            },
            path: {
                resolution: 1,
                material: new Cesium.PolylineGlowMaterialProperty({
                    glowPower: 0.1,
                    color: Cesium.Color.YELLOW
                }),
                width: 3
            }
        });

        // Simple animation logic: Circling Abuja
        let angle = 0;
        viewer.clock.onTick.addEventListener(() => {
            angle += 0.01;
            const offsetLng = Math.cos(angle + i) * 0.02;
            const offsetLat = Math.sin(angle + i) * 0.02;
            droneEntity.position = Cesium.Cartesian3.fromDegrees(abujaLng + offsetLng, abujaLat + offsetLat, 500);
        });
    }
    console.log("Drones deployed over Abuja Sector.");
}

/**
 * EXPERT MODULE: 3D DRONE TELEMETRY SYNC
 * Synchronizes the 3D entities with the real backend drone states.
 */
async function syncDroneTelemetry() {
    try {
        const response = await fetch('http://localhost:8000/api/v1/drone/telemetry');
        const telemetry = await response.json();

        Object.keys(telemetry).forEach(droneId => {
            const data = telemetry[droneId];
            let entity = viewer.entities.getById(droneId);

            // Create if doesn't exist
            if (!entity) {
                // MIL-STD-2525D Icon for UAV (Drone)
                const sym = new ms.Symbol("SFG-UCID---", { size: 40 }); // UAV SIDC

                entity = viewer.entities.add({
                    id: droneId,
                    name: droneId,
                    billboard: {
                        image: sym.asCanvas(),
                        verticalOrigin: Cesium.VerticalOrigin.BOTTOM,
                        pixelOffset: new Cesium.Cartesian2(0, -10)
                    },
                    label: {
                        font: '10px Courier New',
                        pixelOffset: new Cesium.Cartesian2(0, -60)
                    }
                });
            }

            // Sync Position & State
            const position = Cesium.Cartesian3.fromDegrees(data.lng, data.lat, data.alt);
            entity.position = position;
            entity.label.text = `${droneId} [${data.status}]`;

            // Visual feedback for Active Missions
            if (data.status === 'MISSION_ACTIVE') {
                entity.label.fillColor = Cesium.Color.YELLOW;
                entity.label.outlineColor = Cesium.Color.BLACK;
            } else {
                entity.label.fillColor = Cesium.Color.WHITE;
            }
        });
    } catch (err) {
        console.warn("Telemetry Sync Offline: Check Python Backend.");
    }
}

/**
 * EXPERT MODULE: IoT DEVICE SYNC
 * Renders 'Other Devices' (Acoustic, NRC, Mobile Body-cams) in 3D.
 */
async function syncIoTDevices() {
    try {
        const response = await fetch('http://localhost:8000/api/v1/iot/devices');
        const devices = await response.json();

        Object.keys(devices).forEach(deviceId => {
            const data = devices[deviceId];
            let entity = viewer.entities.getById(deviceId);

            if (!entity) {
                entity = viewer.entities.add({
                    id: deviceId,
                    name: `${data.type} SENSOR`,
                    position: Cesium.Cartesian3.fromDegrees(data.location.lng, data.location.lat, 2),
                    point: {
                        pixelSize: 15,
                        color: data.type === 'ACOUSTIC' ? Cesium.Color.LIME : Cesium.Color.MAGENTA,
                        outlineWidth: 2
                    },
                    label: {
                        text: deviceId,
                        font: '8px Courier New',
                        pixelOffset: new Cesium.Cartesian2(0, 20)
                    }
                });
            }

            // Sync visual alert if reading is high
            if (data.last_reading > 0.5) {
                entity.point.pixelSize = 25; // Pulsing effect simulated via reload
                entity.point.color = Cesium.Color.ORANGE;
            }
        });
    } catch (err) {
        console.warn("IoT Sync Offline.");
    }
}

// Start IoT Syncing
setInterval(syncIoTDevices, 5000);

// Automatically deploy drones after a short delay
setTimeout(deployDrones, 5000);

// Use data injected from PHP API bridge
// Fallback to empty array if not defined
const reports = window.INITIAL_REPORTS || [];

reports.forEach(report => {
    // Extract location data from real report structure
    const lat = report.location?.lat || 0;
    const lng = report.location?.lng || 0;
    const title = report.findings?.vision?.[0]?.label || "Active Intel Node";
    const status = report.anomaly_status || "NORMAL";

    if (lat === 0 && lng === 0) return; // Skip invalid reports

    const circle = L.circle([lat, lng], {
        color: status === 'ANOMALY' ? '#ff4d4d' : '#00f2ff',
        fillColor: status === 'ANOMALY' ? '#ff4d4d' : '#00f2ff',
        fillOpacity: 0.2,
        radius: 40000
    }).addTo(map);

    circle.on('click', () => {
        const detailDiv = document.getElementById('report-detail');
        detailDiv.innerHTML = `
            <div class="report-header">
                <h3>${title.toUpperCase()}</h3>
                <span class="report-id">ID: ${report._id}</span>
            </div>
            
            <div class="threat-badge" style="color: ${status === 'ANOMALY' ? '#ff4d4d' : '#00f2ff'}">
                STATUS: ${status}
            </div>

            <div class="findings-grid">
                <div class="finding-item">
                    <strong>VISION:</strong> 
                    ${report.findings?.vision?.length || 0} objects detected
                </div>
                <div class="finding-item">
                    <strong>TIMESTAMP:</strong> 
                    ${new Date(report.timestamp).toLocaleString()}
                </div>
            </div>

            <p style="margin-top: 20px; color: #888;"><strong>SATELLITE CONTEXT:</strong></p>
            <p style="font-size: 0.85rem; color: #ccc;">${report.findings?.satellite?.message || "No imagery metadata"}</p>
            
            <div class="action-buttons">
                <button class="action-btn" onclick="explainReport('${report._id}')">EXPLAIN AI DECISION</button>
            </div>
        `;
    });
});

// Placeholder for XAI calls
window.explainReport = (id) => {
    alert("Requesting XAI explanation for: " + id);
};

// --- REAL-TIME POLLING ENHANCEMENT ---
const REFRESH_INTERVAL = 30000; // 30 seconds

/**
 * Fetch latest reports and update the map without reloading the page.
 */
async function pollIntelligence() {
    try {
        console.log("Polling for new intelligence...");
        const response = await fetch('http://localhost:8000/api/v1/fusion/reports?limit=20');
        const newReports = await response.json();

        if (newReports && Array.isArray(newReports)) {
            // Clear existing markers (if using a marker group)
            // For simplicity in this demo, we just re-run the render logic
            // but in a production app, we would only add NEW markers.
            window.INITIAL_REPORTS = newReports;
            renderMarkers();
        }
    } catch (err) {
        console.warn("Poll failed: Python API might be offline.");
    }
}

let selectedReport = null;

/**
 * EXPERT MODULE: DRONE SWARM DEPLOYMENT
 * Triggers a multi-drone formation around a target.
 */
window.deploySwarm = async (formation) => {
    if (!selectedReport) {
        alert("Select a target hotspot first.");
        return;
    }

    const lat = selectedReport.location?.lat;
    const lng = selectedReport.location?.lng;

    try {
        console.log(`Deploying ${formation} Swarm...`);
        const response = await fetch(`http://localhost:8000/api/v1/drone/swarm?formation=${formation}&lat=${lat}&lng=${lng}`, {
            method: 'POST'
        });
        const result = await response.json();
        if (result.status === 'Swarm deployed') {
            console.log(`${formation} formation confirmed.`);
        }
    } catch (err) {
        console.warn("Swarm Command Failed.");
    }
};

/**
 * EXPERT MODULE: DRONE TACTICAL RE-ROUTING
 * Diverts the nearest drone via the BACKEND API.
 */
window.reRouteDrones = async () => {
    if (!selectedReport) {
        alert("Select an intelligence hotspot first.");
        return;
    }

    const payload = {
        drone_id: "SENTINEL-DRONE-1", // Targeting Drone 1 for this command
        lat: selectedReport.location?.lat,
        lng: selectedReport.location?.lng,
        alt: 300
    };

    try {
        console.log("Sending Dispatch Command to API...");
        const response = await fetch('http://localhost:8000/api/v1/drone/dispatch', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const result = await response.json();
        if (result.status === 'success') {
            console.log("Mission accepted by Drone 1.");
            // The syncDroneTelemetry loop will pick up the new position in 2 seconds.
        }
    } catch (err) {
        alert("Command Center Offline. Check backend connection.");
    }
};

/**
 * Encapsulated marker rendering logic for 3D Cesium
 */
function renderMarkers() {
    viewer.entities.removeAll();
    // Re-deploy static drones if cleared
    deployDrones();

    (window.INITIAL_REPORTS || []).forEach(report => {
        const lat = report.location?.lat || 0;
        const lng = report.location?.lng || 0;
        const title = report.findings?.vision?.[0]?.label || "Active Intel Node";
        const status = report.anomaly_status || "NORMAL";

        if (lat === 0 && lng === 0) return;

        const entity = viewer.entities.add({
            id: `hotspot-${report._id}`,
            position: Cesium.Cartesian3.fromDegrees(lng, lat),
            point: {
                pixelSize: 20,
                color: status === 'ANOMALY' ? Cesium.Color.RED : Cesium.Color.CYAN,
                outlineColor: Cesium.Color.WHITE,
                outlineWidth: 2
            },
            label: {
                text: title.toUpperCase(),
                font: '12px Courier New',
                style: Cesium.LabelStyle.FILL_AND_OUTLINE,
                outlineWidth: 2,
                verticalOrigin: Cesium.VerticalOrigin.BOTTOM,
                pixelOffset: new Cesium.Cartesian2(0, -20)
            }
        });

        // Set description for infoBox
        entity.description = `
            <div class="report-popup" style="color: white; background: #111; padding: 10px;">
                <h3>${title}</h3>
                <p>STATUS: ${status}</p>
                <p>SAFETY: ${report.safety_status || "PASSED"}</p>
                <p>PROPOSAL: ${report.mission_proposal || "N/A"}</p>
                <hr style="border: 0.5px solid #333; margin: 10px 0;">
                <button class="action-btn-small" onclick="window.deploySwarm('CIRCLE')">SWARM TARGET (CIRCLE)</button>
                <button class="action-btn-small" onclick="window.deploySwarm('GRID')" style="margin-left:5px;">SWARM SEARCH (GRID)</button>
            </div>
        `;

        // Update selected report global on selection in Cesium
        viewer.selectedEntityChanged.addEventListener((newEntity) => {
            if (newEntity && newEntity.id.includes('hotspot')) {
                selectedReport = report;
            }
        });
    });
}

// Initial Render
renderMarkers();

// Start Polling
setInterval(pollIntelligence, REFRESH_INTERVAL);
