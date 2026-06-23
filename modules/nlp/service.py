import requests
from faster_whisper import WhisperModel
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
from sentinel_x.core.config import settings
import torch
import json

class NLPService:
    def __init__(self):
        # Initialize faster-whisper (Local OSS)
        self.whisper_model = WhisperModel(settings.WHISPER_MODEL, device="cpu", compute_type="int8")
        
        # Initialize AfroXLMR for multilingual threat detection
        # This model is great for code-switching and Nigerian languages (Hausa, Yoruba, Igbo)
        self.threat_tokenizer = AutoTokenizer.from_pretrained("Davlan/afro-xlmr-large")
        self.classifier = pipeline("sentiment-analysis", model="Davlan/afro-xlmr-large")
        
        # Ollama local API (Open Source LLM Runner)
        self.ollama_url = "http://localhost:11434/api/generate"

    def transcribe_audio(self, audio_path: str):
        """
        Transcribe audio using faster-whisper.
        """
        segments, info = self.whisper_model.transcribe(audio_path, beam_size=5)
        text = " ".join([segment.text for segment in segments])
        return {
            "text": text,
            "language": info.language,
            "probability": info.language_probability
        }

    def analyze_intelligence(self, text: str):
        """
        Perform advanced reasoning on intelligence text using local Ollama LLM.
        """
        prompt = f"Analyze this incident report for national security implications: {text}"
        try:
            response = requests.post(
                self.ollama_url,
                json={"model": "llama3", "prompt": prompt, "stream": False},
                timeout=10
            )
            return response.json().get("response", "Reasoning unavailable.")
        except Exception as e:
            return f"Local Reasoning Offline: {str(e)}"

    def detect_threats(self, text: str):
        """
        Detect threats/violence in text using AfroXLMR.
        """
        results = self.classifier(text)
        return results

nlp_service = NLPService()
