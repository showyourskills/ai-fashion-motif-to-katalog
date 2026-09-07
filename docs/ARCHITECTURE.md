# System Architecture

## Overview

The AI Fashion Motif to Katalog system is designed as a three-stage pipeline with modular components.

```
┌─────────────────────────────────────────────────────────┐
│                   USER INTERFACE                        │
│              React + TypeScript Frontend                │
└────────────────────┬────────────────────────────────────┘
                     │
         ┌──────────��┴───────────┐
         ↓                       ↓
   ┌──────────────┐      ┌──────────────┐
   │ Backend API  │      │ AI Pipeline  │
   │ (Node.js +   │      │  (FastAPI +  │
   │  Express)    │      │  Python)     │
   └──────┬───────┘      └──────┬───────┘
          │                     │
   ┌──────▼─────────────────────▼──────┐
   │       Google Cloud Services        │
   ├────────────────────────────────────┤
   │ • Vision API (Pattern Analysis)   │
   │ • Vertex AI (LLM)                 │
   │ • Cloud Storage                   │
   └────────────────────────────────────┘
          │
   ┌──────▼──────────────────────────┐
   │     AI Model Pipeline            │
   ├──────────────────────────────────┤
   │ Stage 1: Pattern Analysis        │
   │ Stage 2: LLM Prompt Generation   │
   │ Stage 3: Image Generation        │
   └────────────────────────────────────┘
```

## Three-Stage Pipeline

### Stage 1: Pattern Analysis

**Input:** Motif/Pattern Image  
**Output:** Pattern characteristics, color palette, design recommendations

```python
Motif Image
    ↓
[Google Cloud Vision API]
    ↓
Extract:
  - Colors & palette
  - Texture properties
  - Pattern type
  - Style characteristics
    ↓
Analysis Report
```

**Components:**
- `stage1_analysis/pattern_analyzer.py` - Main analysis orchestrator
- `stage1_analysis/color_extractor.py` - Color palette extraction
- `stage1_analysis/texture_classifier.py` - Texture type classification

### Stage 2: LLM Prompt Generation

**Input:** Pattern analysis, clothing type  
**Output:** Design prompt, 3/4 mannequin instructions

```python
Pattern Analysis + User Input
    ↓
[Vertex AI / Google Generative AI]
    ↓
Generate:
  - Design description
  - Mannequin pose instructions
  - Lighting recommendations
  - Style specifications
    ↓
Design Prompt
```

**Components:**
- `stage2_llm/prompt_generator.py` - Prompt creation engine
- `stage2_llm/design_composer.py` - Design context composition
- `stage2_llm/instruction_builder.py` - Mannequin-specific instructions

### Stage 3: Image Generation

**Input:** Design prompt, pattern image (optional)  
**Output:** 3/4 mannequin design (512×512)

```python
Design Prompt + Pattern Control
    ↓
[Stable Diffusion + ControlNet]
    ↓
Generate:
  - High-quality fashion image
  - 3/4 mannequin pose
  - Pattern integration
  - Professional catalog style
    ↓
Final Design Katalog
```

**Components:**
- `stage3_generation/controlnet_pipeline.py` - ControlNet inference
- `stage3_generation/mannequin_generator.py` - Mannequin-specific generation
- `stage3_generation/fine_tuning.py` - Custom model training

---

## Database Schema

### Users Collection
```json
{
  "_id": ObjectId,
  "email": "user@example.com",
  "password_hash": "hashed_password",
  "name": "User Name",
  "created_at": ISODate,
  "updated_at": ISODate
}
```

### Designs Collection
```json
{
  "_id": ObjectId,
  "user_id": ObjectId,
  "motif_image_url": "gs://bucket/motif.png",
  "clothing_type": "dress",
  "analysis": {
    "colors": ["#FF6B6B", "#4ECDC4"],
    "properties": "batik, geometric pattern",
    "description": "..."
  },
  "prompt": "A beautiful 3/4 view fashion...",
  "generated_image_url": "gs://bucket/design.png",
  "metadata": {
    "inference_time": 45.2,
    "model_version": "v1.5"
  },
  "status": "completed",
  "created_at": ISODate,
  "updated_at": ISODate
}
```

### Analytics Collection
```json
{
  "_id": ObjectId,
  "user_id": ObjectId,
  "event_type": "design_generated",
  "design_id": ObjectId,
  "metrics": {
    "stage1_time": 3.2,
    "stage2_time": 8.1,
    "stage3_time": 45.5
  },
  "timestamp": ISODate
}
```

---

## API Flow

### Complete Pipeline Flow

```
1. User uploads motif image via React UI
   ↓
2. Frontend sends to Backend (Node.js)
   POST /api/designs
   ↓
3. Backend stores image in Google Cloud Storage
   ↓
4. Backend calls AI Pipeline (FastAPI)
   POST /api/v1/full-pipeline
   ↓
5. AI Pipeline Stage 1
   - Google Cloud Vision API analyzes motif
   - Returns: colors, properties, description
   ↓
6. AI Pipeline Stage 2
   - Vertex AI generates design prompt
   - Returns: detailed prompt, instructions
   ↓
7. AI Pipeline Stage 3
   - Stable Diffusion + ControlNet generates image
   - Returns: design image URL, metadata
   ↓
8. Backend stores design in MongoDB
   ↓
9. Frontend displays result to user
```

---

## Deployment Architecture

### Development (Docker Compose)

```yaml
Services:
  - frontend (React/Vite) → port 3000
  - backend (Node.js/Express) → port 5000
  - ai_pipeline (FastAPI) → port 8000
  - mongodb → port 27017
```

### Production (Google Cloud)

```
┌─────────────────────────────────────┐
│   Cloud Load Balancer               │
└────────────┬────────────────────────┘
             │
      ┌──────┴──────┬──────────┐
      ↓             ↓          ↓
  ┌────────┐  ┌────────┐  ┌────────┐
  │Frontend│  │Backend │  │AI Pipe │
  │Cloud   │  │Cloud   │  │Cloud   │
  │Storage │  │Run     │  │Run     │
  └────────┘  └────┬───┘  └───┬────┘
                   │          │
              ┌────▼──────────▼────┐
              │  Cloud Storage     │
              └────┬───────────────┘
                   │
              ┌────▼──────────┐
              │ Cloud SQL or  │
              │ MongoDB Atlas │
              └───────────────┘
```

---

## Performance Considerations

### Stage 1: Pattern Analysis
- **Time:** ~3 seconds
- **Bottleneck:** Google Cloud Vision API response
- **Optimization:** Batch processing, caching

### Stage 2: LLM Generation
- **Time:** ~8 seconds
- **Bottleneck:** Token generation
- **Optimization:** Prompt caching, streaming

### Stage 3: Image Generation
- **Time:** ~45 seconds
- **Bottleneck:** Diffusion inference steps
- **Optimization:** LoRA reduction, distillation

### Total End-to-End
- **Time:** ~60 seconds
- **Memory:** ~10GB VRAM
- **Throughput:** 1 design per minute (single GPU)

---

## Error Handling

### Graceful Degradation

```
If Google Cloud Vision fails:
  → Use fallback local image analysis
  → Generate basic prompt from user input

If Vertex AI is unavailable:
  → Use GPT-3.5 turbo (OpenAI) as fallback
  → Use predefined templates

If GPU is unavailable:
  → Use CPU inference (slower but works)
  → Queue processing for later
```

---

## Security Considerations

1. **Authentication:** JWT tokens for API access
2. **Authorization:** User can only access own designs
3. **Data Protection:** Encrypted at rest (Google Cloud)
4. **API Keys:** Never commit to repository, use .env
5. **Rate Limiting:** Prevent abuse via API throttling
6. **Input Validation:** Sanitize all user inputs

---

## Scalability Strategy

### Horizontal Scaling
- Multiple AI Pipeline instances on Cloud Run
- Load balancer distributes requests
- Shared MongoDB for data consistency

### Vertical Scaling
- Use GPU-accelerated Cloud Run
- Increase memory allocation
- Use TPU for inference

### Caching Strategy
- Cache analysis results
- Cache generated prompts
- Cache model weights

---

## Monitoring & Logging

```
Google Cloud Logging:
  - All API requests
  - AI Pipeline metrics
  - Error tracking
  - Performance metrics

Metrics to Monitor:
  - Request latency (per stage)
  - Error rates
  - GPU utilization
  - Memory usage
  - API quota usage
```
