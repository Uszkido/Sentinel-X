const map = L.map('map').setView([9.0820, 8.6753], 6);

L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
    attribution: '&copy; OpenStreetMap &copy; CARTO'
}).addTo(map);

// Simulated data points
const points = [
    { id: 1, lat: 12.0022, lng: 8.5920, title: "Kano Node", threat: "Low", explanation: "Clear vision, normal NDVI" },
    { id: 2, lat: 6.5244, lng: 3.3792, title: "Lagos Node", threat: "High", explanation: "Suspicious vehicle clusters detected" },
    { id: 3, lat: 9.0765, lng: 7.3986, title: "Abuja Core", threat: "Safe", explanation: "All systems operational" }
];

points.forEach(p => {
    const circle = L.circle([p.lat, p.lng], {
        color: p.threat === 'High' ? '#ff4d4d' : '#00f2ff',
        fillColor: p.threat === 'High' ? '#ff4d4d' : '#00f2ff',
        fillOpacity: 0.2,
        radius: 40000
    }).addTo(map);

    circle.on('click', () => {
        document.getElementById('report-detail').innerHTML = `
            <h3>${p.title}</h3>
            <div class="threat-badge" style="color: ${p.threat === 'High' ? '#ff4d4d' : '#00f2ff'}">
                STATUS: ${p.threat.toUpperCase()}
            </div>
            <p style="margin-top: 20px; color: #888;"><strong>XAI Analysis:</strong></p>
            <p style="font-size: 0.9rem; line-height: 1.6;">${p.explanation}</p>
        `;
    });
});
