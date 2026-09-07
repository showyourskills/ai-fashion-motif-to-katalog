# System Architecture — 100% Google Cloud AI Pipeline

## Overview

The AI Fashion Motif to Katalog system is designed as a three-stage cloud-native pipeline powered entirely by **Google Cloud AI** via **Application Default Credentials (ADC)**. 

No dedicated local hardware (GPU, CUDA, or heavy VRAM) is required. All heavy machine learning workloads are executed in Google Cloud.

```
┌─────────────────────────────────────────────────────────┐
│                   USER INTERFACE                        │
│              React + TypeScript Frontend                │
└────────────────────┬────────────────────────────────────┘
                     │
         ┌───────────┴───────────┐
         ↓                       ↓
   ┌──────────────┐      ┌──────────────┐
   │ Backend API  │      │ AI Pipeline  │
   │ (Node.js +   │      │  (FastAPI +  │
   │  Express)    │      │  Python)     │
   └──────┬───────┘      └──────┬───────┘
          │                     │
   ┌──────▼─────────────────────▼─────────────────────────┐
   │           Google Cloud Services (via ADC)            │
   ├──────────────────────────────────────────────────────┤
   │ • Vision API (Motif & Textile Analysis)              │
   │ • Vertex AI Gemini (Catalog Prompt Engineering)      │
   │ • Vertex AI Imagen 3 (High-Res 3/4 Mannequin Render) │
   │ • Cloud Storage (Asset & Image Management)           │
   └──────────────────────────────────────────────────────┘
```

---

## Three-Stage Cloud Pipeline

### Stage 1: Motif & Pattern Analysis (Google Cloud Vision)

**Input:** Motif/Pattern Image  
**Output:** Dominant color palette (HEX/RGB), textile classification, texture properties  
**Authentication:** Google Cloud ADC (`google.auth.default()`)

```
Motif Image (Upload)
    ↓
[Google Cloud Vision API]
    ↓
Extract:
  - Dominant Color Palette (Top 5 Hex/RGB)
  - Textile Properties & Materials
  - Pattern Characteristics
    ↓
Analysis JSON Response
```

**Components:**
- `stage1_analysis/pattern_analyzer.py` — Orchestrator for Vision API & color quantization.

---

### Stage 2: Catalog Prompt Engineering (Google Vertex AI Gemini)

**Input:** Pattern analysis + User preference (clothing type: dress, blazer, kebaya, shirt)  
**Output:** High-precision diffusion prompt optimized specifically for 3/4 mannequin view  
**Authentication:** Google Cloud ADC

```
Analysis Data + Clothing Type
    ↓
[Vertex AI Gemini 1.5/2.0]
    ↓
Synthesize:
  - 3/4 angled minimalist mannequin pose instructions
  - Fabric drape, weave details, seam precision
  - Neutral studio lighting & minimalist gradient backdrop
  - Strict catalog negative prompt (headless/neutral mannequin)
    ↓
Structured Prompt Response
```

**Components:**
- `stage2_llm/prompt_generator.py` — Gemini prompt synthesizer with catalog templates.

---

### Stage 3: Image Generation (Google Vertex AI Imagen 3)

**Input:** Synthesized catalog prompt + optional conditioning  
**Output:** High-resolution 3/4 mannequin catalog photograph  
**Hardware Load:** **0% Local GPU** (fully rendered by Google Cloud infrastructure)  
**Authentication:** Google Cloud ADC

```
Catalog Prompt
    ↓
[Google Vertex AI Imagen 3 API]
    ↓
Generate:
  - High-resolution studio photograph
  - Realistic 3/4 mannequin presentation
  - Seamless motif integration & textile realism
    ↓
Final Catalog Design (PNG/Base64)
```

**Components:**
- `stage3_generation/mannequin_generator.py` — Vertex AI Imagen 3 client with local preview fallback.

---

## API Flow

```
1. User uploads motif image via Frontend (React)
   ↓
2. Request routed to AI Pipeline (FastAPI: POST /api/v1/full-pipeline)
   ↓
3. Stage 1 executes: Google Cloud Vision API analyzes pattern & colors
   ↓
4. Stage 2 executes: Vertex AI Gemini composes 3/4 mannequin catalog prompt
   ↓
5. Stage 3 executes: Vertex AI Imagen 3 generates studio catalog image
   ↓
6. API returns structured JSON:
   - Analysis data
   - Prompt metadata
   - Generated catalog image (Base64 / URL)
```

---

## Hardware & Deployment Specifications

| Metric | Specification |
|---|---|
| **Local GPU Requirement** | **None (0 MB VRAM needed)** |
| **Local CPU/RAM** | Minimal (Standard 2GB–4GB RAM suffices) |
| **Cloud Authentication** | Google Cloud Application Default Credentials (ADC) |
| **Containerization** | Lightweight Python slim Docker image (~200MB) |
| **Cloud Deployment** | Google Cloud Run (Serverless, auto-scaling to zero) |
