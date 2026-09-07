"""
AI Fashion Motif to Katalog - FastAPI AI Service
Entry point REST API untuk 3-Stage Pipeline:
Stage 1 (Pattern Analysis) -> Stage 2 (LLM Prompt) -> Stage 3 (3/4 Mannequin Generation)
"""

from __future__ import annotations
import io
import logging
from typing import Any, Dict, Optional
from fastapi import FastAPI, File, Form, HTTPException, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from PIL import Image

from ai_pipeline.stage1_analysis.pattern_analyzer import PatternAnalyzer
from ai_pipeline.stage2_llm.prompt_generator import PromptGenerator
from ai_pipeline.stage3_generation.mannequin_generator import MannequinGenerator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ai_pipeline")

app = FastAPI(
    title="AI Fashion Motif to Katalog Pipeline API",
    description="Layanan AI pengolah motif pola tekstil menjadi katalog busana manekin 3/4",
    version="1.0.0"
)

# CORS Middleware agar dapat diakses dari Frontend React / Vite
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inisialisasi Service Stages (Singleton Pattern dalam modul)
analyzer_service = PatternAnalyzer()
prompt_service = PromptGenerator()
generator_service = MannequinGenerator()

# Maksimum batas ukuran file upload: 15MB (Validasi batas kepercayaan OWASP)
MAX_FILE_SIZE_BYTES = 15 * 1024 * 1024
ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/webp", "image/bmp"}


def _validate_image_file(file: UploadFile, contents: bytes) -> None:
    """Validasi ketat tipe MIME dan integritas citra pada batas input."""
    if not contents:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File yang diunggah kosong."
        )
    if len(contents) > MAX_FILE_SIZE_BYTES:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="Ukuran file melebihi batas maksimum 15MB."
        )
    if file.content_type and file.content_type.lower() not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"Tipe file {file.content_type} tidak didukung. Harap gunakan JPEG, PNG, atau WebP."
        )


class GeneratePromptRequest(BaseModel):
    analysis: Dict[str, Any] = Field(..., description="Hasil analisis pola dari Stage 1")
    clothing_type: str = Field(default="dress", description="Jenis pakaian (contoh: dress, blazer, kebaya, shirt)")
    style: Optional[str] = Field(default="modern elegant", description="Preferensi gaya busana")


class GenerateDesignRequest(BaseModel):
    prompt: str = Field(..., min_length=5, description="Prompt deskripsi busana")
    negative_prompt: Optional[str] = Field(default="", description="Negative prompt untuk difusi")
    width: Optional[int] = Field(default=512, ge=256, le=1024)
    height: Optional[int] = Field(default=512, ge=256, le=1024)


@app.get("/api/v1/health", summary="Health Check API")
async def health_check():
    """Memeriksa kesiapan dan status seluruh stage pipeline."""
    return {
        "status": "healthy",
        "service": "ai-fashion-pipeline",
        "stages": {
            "stage1_analysis": "ready",
            "stage2_llm": "ready",
            "stage3_generation": "ready"
        }
    }


@app.post("/api/v1/analyze", summary="Stage 1: Analisis Motif & Palet Warna")
async def analyze_motif(file: UploadFile = File(...)):
    """Menerima file gambar motif dan mengekstrak warna dominan & karakteristik tekstil."""
    contents = await file.read()
    _validate_image_file(file, contents)

    try:
        result = analyzer_service.analyze_image_bytes(contents)
        return {"success": True, "data": result}
    except ValueError as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))
    except Exception as err:
        logger.error("Error pada Stage 1 analisis: %s", err)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Gagal menganalisis motif.")


@app.post("/api/v1/generate-prompt", summary="Stage 2: Generasi Prompt Katalog 3/4 Manekin")
async def generate_prompt(payload: GeneratePromptRequest):
    """Menghasilkan prompt terstruktur khusus untuk pemotretan katalog manekin 3/4."""
    try:
        prompt_result = prompt_service.generate_fashion_prompt(
            analysis=payload.analysis,
            clothing_type=payload.clothing_type,
            style_preference=payload.style or "modern elegant"
        )
        return {"success": True, "data": prompt_result}
    except Exception as err:
        logger.error("Error pada Stage 2 prompt: %s", err)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Gagal menyusun prompt busana.")


@app.post("/api/v1/generate-design", summary="Stage 3: Generasi Citra Desain Katalog")
async def generate_design(payload: GenerateDesignRequest):
    """Menghasilkan gambar katalog manekin 3/4 beresolusi tinggi berdasarkan prompt."""
    try:
        design_result = generator_service.generate_design(
            prompt=payload.prompt,
            negative_prompt=payload.negative_prompt or "",
            width=payload.width or 512,
            height=payload.height or 512
        )
        return {"success": True, "data": design_result}
    except Exception as err:
        logger.error("Error pada Stage 3 generasi: %s", err)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Gagal merender citra katalog.")


@app.post("/api/v1/full-pipeline", summary="Full Pipeline: Motif -> Analisis -> Prompt -> Katalog 3/4")
async def run_full_pipeline(
    file: UploadFile = File(..., description="File citra motif/pola batik/kain"),
    clothing_type: str = Form(default="dress", description="Jenis pakaian (blazer, dress, kemeja, dll)"),
    style: str = Form(default="modern elegant", description="Gaya desain")
):
    """
    Eksekusi alur lengkap 3-Stage:
    1. Analisis pola & ekstraksi palet warna dari file motif
    2. Pembuatan prompt terstruktur khusus manekin 3/4
    3. Generasi citra katalog manekin 3/4
    """
    contents = await file.read()
    _validate_image_file(file, contents)

    try:
        # Stage 1: Analisis Motif
        analysis = analyzer_service.analyze_image_bytes(contents)

        # Stage 2: Susun Prompt Busana
        prompt_info = prompt_service.generate_fashion_prompt(
            analysis=analysis,
            clothing_type=clothing_type,
            style_preference=style
        )

        # Stage 3: Render Citra Katalog
        motif_pil = Image.open(io.BytesIO(contents))
        design_output = generator_service.generate_design(
            prompt=prompt_info["prompt"],
            negative_prompt=prompt_info["negative_prompt"],
            pattern_image=motif_pil,
            width=512,
            height=512
        )

        return {
            "success": True,
            "stage1_analysis": analysis,
            "stage2_prompt": prompt_info,
            "stage3_catalog": design_output
        }
    except ValueError as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))
    except Exception as err:
        logger.error("Error pada Full Pipeline: %s", err)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Gagal menjalankan full pipeline.")
