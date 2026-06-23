<?php
/**
 * SENTINEL-X | Command Dashboard
 * This script interacts with the FastAPI Intelligence Core.
 */

// API Configuration
$api_base = "http://localhost:8000/api/v1/fusion";
$reports = [];

try {
    // Fetch real-time intelligence reports from the Python API
    // Note: In production, use cURL for better performance and error handling
    $response = @file_get_contents($api_base . "/reports?limit=20");
    if ($response !== false) {
        $reports = json_decode($response, true);
    }
} catch (Exception $e) {
    // Fallback if API is offline
    $reports = [];
}
?>
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SENTINEL-X | Live Intelligence Map</title>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css" />
    <!-- CesiumJS for Digital Twin 3D (Expert Module) -->
    <script src="https://cesium.com/downloads/cesiumjs/releases/1.105/Build/Cesium/Cesium.js"></script>
    <link href="https://cesium.com/downloads/cesiumjs/releases/1.105/Build/Cesium/Widgets/widgets.css" rel="stylesheet">
    <!-- Military-Standard Symbology (MIL-STD-2525 Support) -->
    <script src="https://unpkg.com/milsymbol@2.1.0/dist/milsymbol.js"></script>
    <link rel="stylesheet" href="css/style.css">
</head>

<body class="dashboard-body">
    <div class="sentinel-dashboard">
        <header class="glass-panel">
            <div class="header-left">
                <a href="index.php" class="back-link">←</a>
                <h1>SENTINEL-X | Command Dashboard</h1>
            </div>
            <div class="status-badge pulse">
                <?php echo empty($reports) ? "API OFFLINE [STANDBY MODE]" : "SYSTEM OPERATIONAL [LIVE INTEL]"; ?>
            </div>
        </header>

        <main>
            <div class="main-content">
                <div id="map" class="map-container"></div>

                <!-- IPC Monitor Grid (New) -->
                <div class="ipc-monitor">
                    <div class="monitor-header">
                        <h3>LIVE IPC MONITOR</h3>
                    </div>
                    <div class="camera-grid">
                        <div class="camera-slot">
                            <div class="cam-label">CAM-01 [ABUJA]</div>
                            <div class="cam-feed placeholder">LOCAL FEED ACTIVE</div>
                        </div>
                        <div class="camera-slot">
                            <div class="cam-label">CAM-02 [LAGOS]</div>
                            <div class="cam-feed placeholder">NO SIGNAL</div>
                        </div>
                        <div class="camera-slot">
                            <div class="cam-label">CAM-03 [KANO]</div>
                            <div class="cam-feed placeholder">ENCRYPTED</div>
                        </div>
                    </div>
                </div>
            </div>

            <aside class="glass-panel sidebar">
                <div class="mission-control-header">
                    <h2>Mission Control</h2>
                    <button class="action-btn-small" onclick="reRouteDrones()">RE-ROUTE DRONES</button>
                </div>
                <div class="spacer"></div>
                <h2>Intelligence Feed</h2>
                <div id="report-detail" class="report-detail">
                    <div class="empty-state">Select a hotspot on the map to analyze</div>
                </div>
            </aside>
        </main>
    </div>

    <!-- Inject PHP Data into JS -->
    <script>
        const INITIAL_REPORTS = <?php echo json_encode($reports); ?>;
    </script>

    <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"></script>
    <script src="js/dashboard.js"></script>
</body>

</html>