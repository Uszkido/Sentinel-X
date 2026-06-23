import datetime
import uuid

class CoTService:
    """
    Cursor-on-Target (CoT) Service for ATAK/WinTAK Integration.
    Generates XML-based tactical events to share intelligence with field officers.
    """
    
    def generate_cot_event(self, lat: float, lng: float, name: str, event_type: str = "a-h-G"):
        """
        Generates a standard CoT Event XML.
        event_type codes:
            'a-h-G': Atom-Hostile-Ground
            'a-u-U-S': Atom-Unknown-Unmanned-Sensor
        """
        now = datetime.datetime.utcnow().isoformat() + "Z"
        stale = (datetime.datetime.utcnow() + datetime.timedelta(minutes=30)).isoformat() + "Z"
        uid = f"SENTINEL-X-{uuid.uuid4().hex[:8]}"
        
        cot_xml = f"""
        <event version="2.0" uid="{uid}" type="{event_type}" time="{now}" start="{now}" stale="{stale}" how="m-g">
            <point lat="{lat}" lon="{lng}" hae="0.0" ce="10.0" le="10.0" />
            <detail>
                <contact callsign="{name}" />
                <remarks>SENTINEL-X AI DETECTED ANOMALY</remarks>
            </detail>
        </event>
        """
        return cot_xml.strip()

cot_service = CoTService()
