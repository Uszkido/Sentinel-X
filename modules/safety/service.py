import re
from typing import List, Dict

class SafetyService:
    """
    Open Source AI Safety & Guardrails Service.
    Enforces policies on intelligence reports to prevent hallucinations 
    and data leakage of sensitive metadata.
    """
    
    def __init__(self):
        # Sensitive patterns (e.g., Nigerian National ID formats, internal server IPs)
        self.sensitive_patterns = [
            r"\b\d{11}\b",  # Potential NIN (National Identification Number)
            r"10\.\d{1,3}\.\d{1,3}\.\d{1,3}", # Internal IPs
            r"192\.168\.\d{1,3}\.\d{1,3}"
        ]
        
        # Policy: Words that should trigger a manual review
        self.red_flag_terms = ["classified", "top secret", "operator-name", "encryption-key"]

    def scrub_sensitive_data(self, text: str) -> str:
        """
        Mask sensitive identifiers in the intelligence reports.
        """
        scrubbed = text
        for pattern in self.sensitive_patterns:
            scrubbed = re.sub(pattern, "[REDACTED]", scrubbed)
        return scrubbed

    def validate_report(self, report: Dict) -> Dict:
        """
        Apply guardrails to a fused intelligence report.
        """
        # 1. Scrub findings
        if "findings" in report:
            for key, val in report["findings"].items():
                if isinstance(val, str):
                    report["findings"][key] = self.scrub_sensitive_data(val)
                elif isinstance(val, dict) and "text" in val:
                    val["text"] = self.scrub_sensitive_data(val["text"])

        # 2. Add safety metadata
        contains_red_flags = any(
            term in str(report).lower() 
            for term in self.red_flag_terms
        )
        report["safety_status"] = "PASSED" if not contains_red_flags else "NEEDS_REVIEW"
        
        return report

safety_service = SafetyService()
