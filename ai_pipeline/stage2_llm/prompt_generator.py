"""
Stage 2: LLM Fashion Prompt Generator
Menerjemahkan analisis motif dan tipe pakaian menjadi prompt terstruktur
khusus untuk pemotretan katalog busana manekin 3/4 (3/4 mannequin fashion catalog).
Mendukung Google Cloud Vertex AI (Gemini) melalui ADC (Application Default Credentials).
"""

from __future__ import annotations
import os
import logging
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

CATALOG_NEGATIVE_PROMPT = (
    "ugly, deformed, disfigured, distorted, blurry, low quality, pixelated, bad anatomy, "
    "unnatural proportions, missing limbs, human head, human eyes, human face, skin blemishes, "
    "watermark, signature, text, noisy background, cluttered background, cartoon, 3d render"
)


class PromptGenerator:
    """Generator prompt katalog busana manekin 3/4 berbasis Google Cloud Vertex AI / Gemini ADC."""

    def __init__(self, project_id: Optional[str] = None, location: Optional[str] = None) -> None:
        self.project_id = project_id or os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GOOGLE_PROJECT_ID")
        self.location = location or os.getenv("VERTEX_AI_REGION", "us-central1")
        self._vertex_model = None
        self._has_vertex = False
        self._init_vertex_ai()

    def _init_vertex_ai(self) -> None:
        """Inisialisasi Vertex AI Gemini menggunakan Google Cloud ADC."""
        try:
            import google.auth
            import vertexai
            from vertexai.generative_models import GenerativeModel

            credentials, discovered_project = google.auth.default()
            project = self.project_id or discovered_project
            if project:
                vertexai.init(project=project, location=self.location, credentials=credentials)
                self._vertex_model = GenerativeModel("gemini-1.5-flash")
                self._has_vertex = True
                logger.info("Vertex AI Gemini terhubung via Google Cloud ADC (Project: %s, Region: %s).", project, self.location)
            else:
                logger.info("Project ID Google Cloud belum terdeteksi. Berjalan dalam mode template prompt.")
        except Exception as e:
            logger.info("Vertex AI ADC belum aktif (%s). Berjalan dalam mode template deterministik.", e)
            self._has_vertex = False

    def generate_fashion_prompt(
        self,
        analysis: Dict[str, Any],
        clothing_type: str = "dress",
        style_preference: str = "modern elegant"
    ) -> Dict[str, Any]:
        """Menghasilkan prompt katalog busana manekin 3/4."""
        if not clothing_type or not clothing_type.strip():
            clothing_type = "dress"
        clothing_type = clothing_type.strip().lower()

        dominant_color = analysis.get("dominant_color", "#4A6B82")
        colors = [c.get("hex", "") for c in analysis.get("colors", []) if isinstance(c, dict)]
        color_str = ", ".join(colors[:4]) if colors else dominant_color
        properties = analysis.get("properties", "intricate textile motif")

        # Coba eksekusi melalui Vertex AI jika ADC aktif
        if self._has_vertex and self._vertex_model:
            try:
                system_instruction = (
                    f"You are an elite fashion designer and catalog art director. "
                    f"A motif textile has dominant colors {color_str} and characteristics: '{properties}'. "
                    f"Compose a high-precision prompt for Google Imagen 3 generating a {clothing_type} in {style_preference} style "
                    f"displayed on a sleek 3/4 angle headless minimalist mannequin in a luxury neutral studio setup. "
                    f"Emphasize fabric drape, realistic weave, clean seams, and professional catalog lighting. "
                    f"Output only the final prompt description."
                )
                response = self._vertex_model.generate_content(system_instruction)
                if response and response.text:
                    custom_prompt = response.text.strip().replace("\n", ", ")
                    return {
                        "prompt": custom_prompt,
                        "negative_prompt": CATALOG_NEGATIVE_PROMPT,
                        "clothing_type": clothing_type,
                        "dominant_colors": colors,
                        "target_pose": "3/4 view mannequin pose",
                        "engine": "google-vertex-gemini (ADC)"
                    }
            except Exception as e:
                logger.warning("Panggilan Vertex AI Gemini gagal (%s), fallback ke template katalog.", e)

        # ponytail: Template prompt berkualitas tinggi untuk katalog manekin 3/4
        base_prompt = (
            f"professional catalog fashion photography, elegant 3/4 angle view of a sleek minimalist mannequin, "
            f"wearing a bespoke {style_preference} {clothing_type}, adorned with precise textile pattern inspired by "
            f"{properties}, dominant color palette {color_str}, hyper-detailed fabric drape, fine seams and stitching, "
            f"soft studio lighting, neutral grey gradient studio background, 8k resolution, shot on Hasselblad, crisp sharp focus"
        )

        return {
            "prompt": base_prompt,
            "negative_prompt": CATALOG_NEGATIVE_PROMPT,
            "clothing_type": clothing_type,
            "dominant_colors": colors,
            "target_pose": "3/4 view mannequin pose",
            "engine": "deterministic-template"
        }
