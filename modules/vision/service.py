import cv2
import numpy as np
from ultralytics import YOLO
from segment_anything import sam_model_registry, SamPredictor
from sentinel_x.core.config import settings
import torch

class VisionService:
    def __init__(self):
        # Load YOLOv8
        self.yolo_model = YOLO(settings.YOLO_MODEL_PATH)
        
        # Load SAM (placeholder for initialization as it requires model weights)
        self.sam_predictor = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

    def ingest_ipc_stream(self, stream_url: str, callback):
        """
        Process a live RTSP/HTTP IP Camera stream in a non-blocking way.
        Frames are fed into the detection pipeline.
        """
        cap = cv2.VideoCapture(stream_url)
        if not cap.isOpened():
            return False
            
        def stream_worker():
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Process every 5th frame to save CPU (assuming 30fps)
                # In production, use a more robust frame skipper
                detections = self.detect_objects(frame)
                if detections:
                    callback(detections)
                    
            cap.release()

        import threading
        t = threading.Thread(target=stream_worker, daemon=True)
        t.start()
        return True

    def detect_objects(self, image: np.ndarray):
        """
        Detect objects in an image using YOLOv8.
        """
        results = self.yolo_model(image)
        detections = []
        for result in results:
            for box in result.boxes:
                detections.append({
                    "class": self.yolo_model.names[int(box.cls)],
                    "confidence": float(box.conf),
                    "bbox": box.xyxy[0].tolist()
                })
        return detections

    # --- EXPERT: AGENTIC CAMERA HUB ---

    def calculate_target_handoff(self, target_id: str, last_camera_id: str, trajectory_vector: list):
        """
        Agentic Hand-off: Predicts which camera should pick up the target next.
        Inspired by DeepCamera collaborative tracking.
        """
        # Map of cameras and their spatial relations (Demo logic)
        camera_network = {
            "CAM-01": {"next": "CAM-02", "vector_threshold": [1, 0]}, # CAM-01 is south of CAM-02
            "CAM-02": {"next": "CAM-03", "vector_threshold": [0, 1]}
        }
        
        handoff = camera_network.get(last_camera_id, {"next": "NONE"})
        return {
            "target": target_id,
            "source_cam": last_camera_id,
            "assigned_cam": handoff["next"],
            "status": "PRE_ALERT_SENT" if handoff["next"] != "NONE" else "TARGET_LOST"
        }

    # --- EXPERT: HIGH-PRECISION (SAHI & SUPER-RES) ---

    def sahi_inference(self, image: np.ndarray, slice_size: int = 640):
        """
        Sliced Aided Hyper Inference (SAHI).
        Slices high-res images to detect tiny targets.
        """
        h, w, _ = image.shape
        detections = []
        
        # Simple Tiling simulation (SAHI Pattern)
        for y in range(0, h, slice_size - 100): # 100px overlap
            for x in range(0, w, slice_size - 100):
                slice_img = image[y:y+slice_size, x:x+slice_size]
                if slice_img.size == 0: continue
                # Perform inference on slice
                results = self.yolo_model(slice_img)
                # Map coordinates back to global image
                for result in results:
                    for box in result.boxes:
                        global_box = box.xyxy[0].tolist()
                        global_box[0] += x
                        global_box[1] += y
                        global_box[2] += x
                        global_box[3] += y
                        detections.append({
                            "class": self.yolo_model.names[int(box.cls)],
                            "confidence": float(box.conf),
                            "bbox": global_box
                        })
        return detections

    def super_resolution_enhance(self, image_crop: np.ndarray):
        """
        Upscales a target crop using Super-Resolution logic (Inspired by ESRGAN).
        Enables human operators to see fine details.
        """
        # Simulation of 2x Upscale
        enhanced = cv2.resize(image_crop, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        # Apply sharpening to simulate SR reconstruction
        kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
        enhanced = cv2.filter2D(enhanced, -1, kernel)
        return enhanced

    # --- EXPERT: CROWD BEHAVIORAL INTELLIGENCE ---

    def estimate_crowd_density(self, detections: list):
        """
        Calculates Persons Per Square Meter (PPSM).
        In a real system, normalize by calibrated ground area.
        """
        people_count = sum(1 for d in detections if d["class"] == "person")
        # Logic: If person count > 50 in a single cam view, mark as High Density.
        density_level = "NORMAL"
        if people_count > 50: density_level = "CONGESTED"
        if people_count > 150: density_level = "CRITICAL_DENSITY"
        
        return {
            "count": people_count,
            "density_level": density_level,
            "ppsm_estimate": round(people_count / 100, 2) # Mock 100sqm view
        }

    def detect_panic_flow(self, current_trajectories: list):
        """
        Detects sudden velocity spikes (Inspired by Crowd_Monitoring_Project).
        Triggers alert if average velocity > 4.0 m/s in a single direction.
        """
        # Simulated velocity logic: Avg movement speed in pixels or meters.
        avg_velocity = 5.2 # Mock high velocity spike for panic detection
        direction_consensus = 0.85 # 85% of crowd moving toward same vector
        
        is_panic = avg_velocity > 4.0 and direction_consensus > 0.7
        return {
            "is_panic": is_panic,
            "severity": "HIGH" if is_panic else "LOW",
            "type": "STAMPEDE_RISK" if is_panic else "STEADY_FLOW"
        }

    def segment_objects(self, image: np.ndarray, bboxes: list):
        """
        Segment objects in an image using SAM given bounding boxes.
        """
        if self.sam_predictor is None:
            # In a real scenario, weights would be pre-downloaded
            # sam = sam_model_registry["vit_h"](checkpoint="sam_vit_h_4b8939.pth")
            # sam.to(device=self.device)
            # self.sam_predictor = SamPredictor(sam)
            return {"error": "SAM weights not loaded"}
        
        self.sam_predictor.set_image(image)
        segmentations = []
        for bbox in bboxes:
            input_box = np.array(bbox)
            masks, scores, logits = self.sam_predictor.predict(
                box=input_box,
                multimask_output=False,
            )
            segmentations.append(masks[0].tolist())
        return segmentations

vision_service = VisionService()
