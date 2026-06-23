from sentinel_x.modules.vision.service import vision_service
from sentinel_x.modules.nlp.service import nlp_service
from sentinel_x.modules.satellite.service import satellite_service
from sentinel_x.modules.fusion.anomaly import anomaly_detector
from sentinel_x.modules.safety.service import safety_service
from sentinel_x.modules.generative.service import generative_service
from sentinel_x.modules.integrity.service import integrity_service
from sentinel_x.modules.drone.service import drone_service
from sentinel_x.modules.vision.reid import reid_service
from sentinel_x.modules.iot.service import iot_service
from sentinel_x.modules.cot.service import cot_service
from sentinel_x.db.mongodb import get_database
from datetime import datetime
import numpy as np
import cv2

class FusionService:
    async def process_intelligence(self, image_bytes: bytes = None, audio_path: str = None, location: dict = None):
        """
        Orchestrate multiple AI pillars to produce a fused intelligence report.
        """
        report = {
            "timestamp": datetime.utcnow().isoformat(),
            "location": location,
            "findings": {}
        }

        # 2. Vision Analysis (with HIGH-PRECISION SAHI)
        if image_bytes:
            nparr = np.frombuffer(image_bytes, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            # Use SAHI Tiling for small targets
            precision_detections = vision_service.sahi_inference(img)
            report["findings"]["precision_vision"] = precision_detections
            
            # CROWD BEHAVIORAL INTELLIGENCE (Expert Module)
            report["findings"]["crowd_density"] = vision_service.estimate_crowd_density(precision_detections)
            panic_report = vision_service.detect_panic_flow([]) # Mock list
            report["findings"]["crowd_behavior"] = panic_report
            
            # AUTO-RESPONSE to Crowd Panic
            if panic_report["is_panic"] and location:
                drone_service.execute_swarm_mission("GRID", location["lat"], location["lng"])
            
            # Generate Person Re-ID Signature (Expert Module)
            report["reid_signature"] = reid_service.generate_soft_signature(img[0:100, 0:100]) # Mock crop

        # 3. Acoustic Triangulation (Kinetic Response)
        # Simulate local network detection of high decibel event
        acoustic_events = [
            {"device_id": "ACOUSTIC-ABJ-01", "intensity": 0.9},
            {"device_id": "ACOUSTIC-ABJ-02", "intensity": 0.7}
        ]
        triangulation = iot_service.triangulate_acoustic_source(acoustic_events)
        if triangulation:
            report["findings"]["acoustic_triangulation"] = triangulation
            # AUTO-SWARM Dispatch to kinetic origin
            drone_service.execute_swarm_mission("CIRCLE", triangulation["origin"]["lat"], triangulation["origin"]["lng"])

        # 4. ATAK Support (Cursor-on-Target)
        if location:
            report["cot_payload"] = cot_service.generate_cot_event(
                location["lat"], location["lng"], 
                report["findings"].get("precision_vision", [{}])[0].get("class", "Target")
            )

        # 5. Satellite Context & Agrarian Prediction
        if audio_path:
            transcription = nlp_service.transcribe_audio(audio_path)
            report["findings"]["nlp"] = transcription
            
            # Cognitive Security: Check for Deepfake/Synthetic Audio
            report["findings"]["integrity"] = integrity_service.check_information_integrity(transcription["text"])
            
            # Use Local LLM (Ollama) for reasoning if text is available
            report["findings"]["reasoning"] = nlp_service.analyze_intelligence(transcription["text"])

        # 5. Satellite Analysis
        if location:
            report["findings"]["satellite"] = satellite_service.search_imagery(
                footprint=str(location), 
                date_range=("NOW-1MONTH", "NOW")
            )
            # Proactive Agrarian Conflict Prediction
            mock_drift = [{"name": "Monitoring Sector", "ndvi_drift": -0.25}] 
            report["findings"]["agrarian_risk"] = satellite_service.predict_conflict_zones(mock_drift)
            report["findings"]["structural_change"] = satellite_service.perform_change_detection(str(location), "REF_DATA_2026_01")

        # 6. Anomaly Detection Engine
        vision_count = len(report["findings"].get("precision_vision", []))
        nlp_prob = report.get("findings", {}).get("nlp", {}).get("probability", 0)
        integrity_score = report.get("findings", {}).get("integrity", {}).get("integrity_score", 1.0)
        
        features = [vision_count, nlp_prob, integrity_score]
        report["anomaly_status"] = "ANOMALY" if anomaly_detector.detect(features) == -1 else "NORMAL"

        # 7. Agentic Generative Intelligence
        if report["anomaly_status"] == "ANOMALY":
            intel_context = str(report["findings"])
            report["proactive_scenario"] = generative_service.generate_proactive_scenario(intel_context)
            report["mission_proposal"] = generative_service.propose_intelligence_mission(intel_context)
            
            # Autonomous Swarm/Drone Dispatch
            if location:
                report["drone_dispatch"] = drone_service.autonomous_dispatch(location["lat"], location["lng"])

        # 8. Open Source Guardrails (Safety & Ethics)
        report = safety_service.validate_report(report)

        # 7. Save to MongoDB
        db = get_database()
        if db is not None:
            await db.intelligence.insert_one(report)
            
        return report

fusion_service = FusionService()
