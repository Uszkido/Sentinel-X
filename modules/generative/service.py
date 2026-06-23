import requests
from sentinel_x.core.config import settings

class GenerativeService:
    """
    Generative AI Service for Sentinel-X.
    Handles synthetic data generation, forensic sketching, and automated scenario reporting.
    """
    def __init__(self):
        # We can use local Stable Diffusion (via API) or Ollama for Multimodal
        self.sd_api_url = "http://localhost:7860/sdapi/v1/txt2img"
        self.ollama_url = "http://localhost:11434/api/generate"

    def generate_forensic_sketch(self, description: str):
        """
        Generate a forensic situational sketch based on a textual description of a threat.
        Uses local Stable Diffusion API.
        """
        prompt = f"Forensic high-quality security sketch of: {description}, security camera style, monochrome"
        try:
            # Placeholder for actual SD API call
            # response = requests.post(self.sd_api_url, json={"prompt": prompt})
            # return response.json()['images'][0]
            return {"status": "Generating sketch...", "prompt": prompt}
        except Exception:
            return {"error": "Generative Node Offline"}

    def generate_proactive_scenario(self, intelligence_context: str):
        """
        Generate a proactive risk scenario for peacebuilding and mitigation.
        Uses local Ollama (Llama 3).
        """
        prompt = f"Based on this intel: {intelligence_context}. Generate 3 proactive mitigation strategies to prevent conflict."
        try:
            response = requests.post(
                self.ollama_url,
                json={"model": "llama3", "prompt": prompt, "stream": False},
                timeout=15
            )
            return response.json().get("response", "Scenario generation failed.")
        except Exception as e:
            return f"Offline: {str(e)}"

    def propose_intelligence_mission(self, historical_context: str):
        """
        The model analyzes long-term trends and proposes a new 'Intelligence Mission' 
        (e.g., 'Increase drone monitoring in sector 4 due to rising anomalies').
        """
        prompt = f"Analyze these historical trends and propose a new strategic intelligence mission for Sentinel-X: {historical_context}"
        try:
            response = requests.post(
                self.ollama_url,
                json={"model": "llama3", "prompt": prompt, "stream": False},
                timeout=15
            )
            return response.json().get("response", "No proposals at this time.")
        except Exception:
            return "Mission Proposal System Standby."

    def teach_model_logic(self, unclear_data: str):
        """
        Active Learning: Use the powerful Generative LLM to 'teach' smaller models 
        by auto-labeling data they were uncertain about.
        """
        prompt = f"Act as an expert annotator. The vision model is unsure about this detection. Label it accurately for training: {unclear_data}"
        try:
            response = requests.post(
                self.ollama_url,
                json={"model": "llama3", "prompt": prompt, "stream": False},
                timeout=10
            )
            return response.json().get("response", "Labeling failed.")
        except Exception:
            return "Auto-Annotator Standby."

generative_service = GenerativeService()
