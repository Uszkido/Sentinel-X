<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SENTINEL-X | Live Intelligence Map</title>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css" />
    <link rel="stylesheet" href="css/style.css">
</head>

<body class="dashboard-body">
    <div class="sentinel-dashboard">
        <header class="glass-panel">
            <div class="header-left">
                <a href="index.php" class="back-link">←</a>
                <h1>SENTINEL-X | Command Dashboard</h1>
            </div>
            <div class="status-badge pulse">SYSTEM OPERATIONAL [PHP CORE]</div>
        </header>

        <main>
            <div id="map" class="map-container"></div>

            <aside class="glass-panel sidebar">
                <h2>Intelligence Feed</h2>
                <div id="report-detail" class="report-detail">
                    <div class="empty-state">Select a hotspot on the map to analyze</div>
                </div>
            </aside>
        </main>
    </div>

    <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"></script>
    <script src="js/dashboard.js"></script>
</body>

</html>