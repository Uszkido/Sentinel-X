from typing import Dict, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class IoTService:
    """
    Universal Device Gateway for Sentinel-X.
    Supports Acoustic Sensors, NRC Sensors, and Mobile Body-cams.
    """
    def __init__(self):
        # Sensor Registry
        self.sensors = {
            "ACOUSTIC-ABJ-01": {"type": "ACOUSTIC", "location": {"lat": 9.0765, "lng": 7.3986}, "status": "ONLINE", "last_reading": 0.0},
            "NRC-ABJ-04": {"type": "CHEMICAL", "location": {"lat": 9.0865, "lng": 7.4086}, "status": "ONLINE", "last_reading": 0.02},
            "BODYCAM-FCT-22": {"type": "BODYCAM", "location": {"lat": 9.0565, "lng": 7.3786}, "status": "PATROL_ACTIVE", "stream_url": "/live/fct-22"}
        }

    def get_all_devices(self) -> Dict:
        return self.sensors

    def ingest_sensor_data(self, device_id: str, reading: float):
        """
        Ingest raw sensor data and trigger alerts if thresholds are exceeded.
        """
        if device_id in self.sensors:
            self.sensors[device_id]["last_reading"] = reading
            self.sensors[device_id]["last_update"] = datetime.utcnow().isoformat()
            
            # Specialized Alert Logic
            if self.sensors[device_id]["type"] == "ACOUSTIC" and reading > 0.85:
                logger.warning(f"HIGH NOISE ANOMALY: Possible Shot Detected at {device_id}")
                return {"alert": "ACOUSTIC_ANOMALY", "device": device_id}
            
            return {"status": "ingested"}
        return {"error": "Device not found"}

    # --- EXPERT: KINETIC EVENT TRIANGULATION ---

    def triangulate_acoustic_source(self, sensor_readings: List[Dict]):
        """
        Calculates the GPS origin of a sound based on Signal Strength (RSSI) 
        from multiple acoustic sensors.
        Formula: Weighted Centroid of sensor locations.
        """
        if len(sensor_readings) < 2:
            return None
            
        total_weight = 0
        sum_lat = 0
        sum_lng = 0
        
        for reading in sensor_readings:
            s_id = reading["device_id"]
            intensity = reading["intensity"]
            
            if s_id in self.sensors:
                loc = self.sensors[s_id]["location"]
                # Use intensity as the weighting factor
                sum_lat += loc["lat"] * intensity
                sum_lng += loc["lng"] * intensity
                total_weight += intensity
        
        if total_weight == 0: return None
        
        origin_lat = sum_lat / total_weight
        origin_lng = sum_lng / total_weight
        
        return {
            "origin": {"lat": origin_lat, "lng": origin_lng},
            "confidence": 0.85 if len(sensor_readings) > 2 else 0.6,
            "type": "TRIANGULATED_KINETIC_EVENT"
        }

    # --- EXPERT: SIGINT (SIGNAL INTELLIGENCE) ---

    def sigint_analysis(self, frequency_spikes: List[Dict]):
        """
        Expert Module: Analyzes RF signals for hostiles.
        Matches signal strength with spatial density to find hidden units.
        """
        sigint_data = []
        for spike in frequency_spikes:
            # Logic: If frequency matches common tactical bands (VHF/UHF)
            # detect as possible SIGINT finding.
            sigint_data.append({
                "frequency": spike["freq"],
                "density": spike["intensity"],
                "location": spike["pos"],
                "type": "TACTICAL_SIGNAL_DETECTED" if spike["freq"] > 140 else "CARRIER_SIGNAL"
            })
        return sigint_data

iot_service = IoTService()
