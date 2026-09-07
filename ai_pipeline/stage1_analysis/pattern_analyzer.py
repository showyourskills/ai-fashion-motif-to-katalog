"""
Stage 1: Motif & Pattern Analyzer
Ekstraksi palet warna dominan dan analisis karakteristik tekstil/motif.
Mendukung Google Cloud Vision API melalui Application Default Credentials (ADC),
dengan graceful fallback ke analisis lokal (Ponytail Mode).
"""

from __future__ import annotations
import io
import os
import logging
from typing import Any, Dict, List, Tuple
from PIL import Image

logger = logging.getLogger(__name__)


def _rgb_to_hex(r: int, g: int, b: int) -> str:
    """Mengubah nilai RGB menjadi format string hex (#RRGGBB)."""
    return f"#{r:02x}{g:02x}{b:02x}".upper()


def extract_dominant_colors(image: Image.Image, num_colors: int = 5) -> List[Dict[str, Any]]:
    """
    Mengekstrak palet warna dominan dari gambar menggunakan Pillow adaptive palette.
    Hemat komputasi dan tidak memerlukan dependency besar.
    """
    thumb = image.convert("RGB").resize((150, 150))
    # ponytail: Pillow adaptive quantization sangat cepat dan hemat resource
    quantized = thumb.quantize(colors=num_colors, method=Image.Quantize.FASTOCTREE)
    palette = quantized.getpalette()[: num_colors * 3]
    color_counts = quantized.getcolors()

    if not color_counts:
        return [{"hex": "#FFFFFF", "rgb": [255, 255, 255], "percentage": 100.0}]

    total_pixels = sum(count for count, _ in color_counts)
    sorted_colors = sorted(color_counts, key=lambda item: item[0], reverse=True)

    results = []
    for count, idx in sorted_colors[:num_colors]:
        r = palette[idx * 3]
        g = palette[idx * 3 + 1]
        b = palette[idx * 3 + 2]
        percentage = round((count / total_pixels) * 100, 2)
        results.append({
            "hex": _rgb_to_hex(r, g, b),
            "rgb": [r, g, b],
            "percentage": percentage
        })

    return results


class PatternAnalyzer:
    """Orkestrator analisis motif kain dan busana via Google Cloud Vision ADC."""

    def __init__(self) -> None:
        self._has_gcp_vision = False
        self._vision_client = None
        self._init_vision_client()

    def _init_vision_client(self) -> None:
        """Inisialisasi Google Cloud Vision client menggunakan ADC atau kredensial default."""
        try:
            import google.auth
            from google.cloud import vision
            # Coba dapatkan kredensial default ADC (gcloud auth application-default login)
            credentials, project = google.auth.default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
            self._vision_client = vision.ImageAnnotatorClient(credentials=credentials)
            self._has_gcp_vision = True
            logger.info("Google Cloud Vision API terhubung dengan Google Cloud ADC (Project: %s).", project)
        except Exception as e:
            logger.info("Google Cloud ADC belum terkonfigurasi (%s). Berjalan dalam mode analisis lokal.", e)
            self._has_gcp_vision = False

    def analyze_image_bytes(self, image_bytes: bytes) -> Dict[str, Any]:
        """Menganalisis byte gambar motif: validasi batas input dan ekstraksi karakteristik."""
        if not image_bytes:
            raise ValueError("Input data gambar kosong.")

        try:
            image = Image.open(io.BytesIO(image_bytes))
            image.verify()
            image = Image.open(io.BytesIO(image_bytes))
        except Exception as e:
            raise ValueError(f"Format citra tidak valid atau rusak: {e}")

        colors = extract_dominant_colors(image, num_colors=5)
        dominant_hex = colors[0]["hex"] if colors else "#333333"
        labels, properties = self._extract_properties(image_bytes, colors)

        return {
            "dimensions": {"width": image.width, "height": image.height},
            "format": image.format or "JPEG",
            "colors": colors,
            "dominant_color": dominant_hex,
            "labels": labels,
            "properties": properties,
            "auth_mode": "Google Cloud ADC" if self._has_gcp_vision else "Local Fallback",
            "description": f"Motif kain dengan warna dominan {dominant_hex} dan aksen {', '.join([c['hex'] for c in colors[1:3]])}."
        }

    def _extract_properties(
        self, image_bytes: bytes, colors: List[Dict[str, Any]]
    ) -> Tuple[List[str], str]:
        """Ekstraksi label & properti tekstil melalui Google Cloud Vision API atau Heuristik."""
        if self._has_gcp_vision and self._vision_client:
            try:
                from google.cloud import vision
                vision_image = vision.Image(content=image_bytes)
                response = self._vision_client.label_detection(image=vision_image)
                labels = [label.description for label in response.label_annotations][:6]
                if labels:
                    return labels, f"Tekstil terdeteksi via Cloud Vision: {', '.join(labels)}"
            except Exception as e:
                logger.warning("Panggilan Vision API gagal: %s. Menggunakan analisis lokal.", e)

        hex_list = [c["hex"] for c in colors]
        heuristic_labels = ["textile", "pattern", "motif", "fashion fabric", "intricate print"]
        properties_desc = f"Pola motif kaya tekstur dengan variasi warna {', '.join(hex_list[:3])}"
        return heuristic_labels, properties_desc
