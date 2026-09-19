import os
import yaml
from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class AISystemProfile:
    name: str
    sector: str
    uses_biometrics: bool
    is_customer_facing: bool
    generates_synthetic_content: bool
    target_audience: str

class ManifestParser:
    """
    Parses and validates the ai-manifest.yaml configuration file from a project repository.
    """
    
    @staticmethod
    def parse_manifest(file_path: str = "ai-manifest.yaml") -> AISystemProfile:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Missing required compliance file: {file_path}")

        try:
            with open(file_path, "r") as f:
                data = yaml.safe_load(f) or {}
        except yaml.YAMLError as e:
            raise ValueError(f"Error parsing YAML syntax in {file_path}: {e}")

        # Basic schema validation / default fallbacks
        try:
            return AISystemProfile(
                name=data.get("name", "Unnamed AI System"),
                sector=data.get("sector", "General"),
                uses_biometrics=bool(data.get("uses_biometrics", False)),
                is_customer_facing=bool(data.get("is_customer_facing", False)),
                generates_synthetic_content=bool(data.get("generates_synthetic_content", False)),
                target_audience=data.get("target_audience", "general public")
            )
        except Exception as e:
            raise ValueError(f"Invalid fields in {file_path}: {e}")
