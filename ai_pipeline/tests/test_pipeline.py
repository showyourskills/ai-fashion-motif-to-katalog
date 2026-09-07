"""
Unit & Integration Tests untuk AI Fashion Pipeline
Memverifikasi fungsionalitas Stage 1, Stage 2, Stage 3, dan endpoint FastAPI
sesuai dengan aturan Non-Negotiable AGENTS.md (Runnable Check).
"""

from __future__ import annotations
import io
import pytest
from PIL import Image, ImageDraw
from fastapi.testclient import TestClient

from ai_pipeline.app import app
from ai_pipeline.stage1_analysis.pattern_analyzer import PatternAnalyzer, extract_dominant_colors
from ai_pipeline.stage2_llm.prompt_generator import PromptGenerator
from ai_pipeline.stage3_generation.mannequin_generator import MannequinGenerator


@pytest.fixture
def sample_motif_image_bytes() -> bytes:
    """Membuat citra motif sintetis (batik/garis warna-warni) untuk pengujian."""
    img = Image.new("RGB", (200, 200), color=(180, 50, 50))
    draw = ImageDraw.Draw(img)
    # Tambahkan pola garis warna kontras
    draw.rectangle([50, 50, 150, 150], fill=(50, 120, 200))
    draw.ellipse([70, 70, 130, 130], fill=(220, 180, 60))

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


# ==========================================
# 1. UNIT TESTS: STAGE 1 (ANALISIS MOTIF)
# ==========================================

def test_extract_dominant_colors(sample_motif_image_bytes):
    img = Image.open(io.BytesIO(sample_motif_image_bytes))
    colors = extract_dominant_colors(img, num_colors=3)
    assert isinstance(colors, list)
    assert len(colors) >= 1
    assert "hex" in colors[0]
    assert colors[0]["hex"].startswith("#")
    assert "rgb" in colors[0]
    assert len(colors[0]["rgb"]) == 3


def test_pattern_analyzer_valid(sample_motif_image_bytes):
    analyzer = PatternAnalyzer()
    result = analyzer.analyze_image_bytes(sample_motif_image_bytes)

    assert result["dimensions"]["width"] == 200
    assert result["dimensions"]["height"] == 200
    assert result["dominant_color"].startswith("#")
    assert len(result["colors"]) > 0
    assert isinstance(result["labels"], list)
    assert len(result["properties"]) > 0


def test_pattern_analyzer_invalid_bytes():
    analyzer = PatternAnalyzer()
    with pytest.raises(ValueError):
        analyzer.analyze_image_bytes(b"not-an-image-data")


# ==========================================
# 2. UNIT TESTS: STAGE 2 (PROMPT GENERATOR)
# ==========================================

def test_prompt_generator():
    generator = PromptGenerator()
    dummy_analysis = {
        "dominant_color": "#B43232",
        "colors": [{"hex": "#B43232"}, {"hex": "#3278C8"}],
        "properties": "pola batik tradisional merah dan biru"
    }
    result = generator.generate_fashion_prompt(
        analysis=dummy_analysis,
        clothing_type="blazer",
        style_preference="formal modern"
    )

    assert "blazer" in result["prompt"].lower()
    assert "3/4" in result["prompt"] or "mannequin" in result["prompt"].lower()
    assert result["clothing_type"] == "blazer"
    assert len(result["negative_prompt"]) > 0


# ==========================================
# 3. UNIT TESTS: STAGE 3 (MANNEQUIN GENERATOR)
# ==========================================

def test_mannequin_generator(sample_motif_image_bytes):
    generator = MannequinGenerator()
    motif_img = Image.open(io.BytesIO(sample_motif_image_bytes))

    output = generator.generate_design(
        prompt="A 3/4 mannequin in elegant batik blazer",
        negative_prompt="ugly, blurry",
        pattern_image=motif_img,
        width=512,
        height=512
    )

    assert "image_base64" in output
    assert len(output["image_base64"]) > 100
    assert output["width"] == 512
    assert output["height"] == 512
    assert output["inference_time_seconds"] >= 0


# ==========================================
# 4. INTEGRATION TESTS: FASTAPI API ENDPOINTS
# ==========================================

def test_api_health(client):
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "stage1_analysis" in data["stages"]


def test_api_analyze_endpoint(client, sample_motif_image_bytes):
    response = client.post(
        "/api/v1/analyze",
        files={"file": ("motif.png", sample_motif_image_bytes, "image/png")}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "dominant_color" in data["data"]


def test_api_generate_prompt_endpoint(client):
    payload = {
        "analysis": {
            "dominant_color": "#112233",
            "colors": [{"hex": "#112233"}],
            "properties": "geometric motif"
        },
        "clothing_type": "kebaya",
        "style": "haute couture"
    }
    response = client.post("/api/v1/generate-prompt", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "kebaya" in data["data"]["prompt"].lower()


def test_api_full_pipeline(client, sample_motif_image_bytes):
    response = client.post(
        "/api/v1/full-pipeline",
        files={"file": ("motif.png", sample_motif_image_bytes, "image/png")},
        data={"clothing_type": "evening gown", "style": "contemporary"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "stage1_analysis" in data
    assert "stage2_prompt" in data
    assert "stage3_catalog" in data
    assert "image_base64" in data["stage3_catalog"]


def test_api_invalid_file_type(client):
    response = client.post(
        "/api/v1/analyze",
        files={"file": ("document.pdf", b"%PDF-1.4 dummy content", "application/pdf")}
    )
    assert response.status_code == 415  # Unsupported Media Type
