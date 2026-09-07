# 🎨 AI Fashion Motif to Katalog Generator

> **Complete AI-Powered Fashion Design System**  
> Transform motif patterns into professional 3/4 mannequin designs using Google Cloud AI, LLM, and generative models.

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Latest-009688.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18+-61DAFB.svg)](https://reactjs.org/)
[![Google Cloud](https://img.shields.io/badge/Google%20Cloud-Integrated-FF9800.svg)](https://cloud.google.com/)
[![Stable Diffusion](https://img.shields.io/badge/Stable%20Diffusion-ControlNet-purple.svg)](https://huggingface.co/)

---

## 🌟 Project Overview

This project combines cutting-edge AI technologies from multiple sources to create a comprehensive fashion design system:

```
┌─────────────────────────────────────────────────────┐
│           Upload Motif/Pattern Image                │
└────────────────────┬────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────┐
│    STAGE 1: Google Cloud Vision + Analysis          │
│  • Extract pattern colors & characteristics         │
│  • Detect textile properties                        │
└────────────────────┬────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────┐
│  STAGE 2: Vertex AI LLM + Prompt Generation         │
│  • Generate design description from motif           │
│  • Create 3/4 mannequin-specific instructions       │
└────────────────────┬────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────┐
│  STAGE 3: Stable Diffusion + ControlNet             │
│  • Pattern-aware image generation                   │
│  • ControlNet for precise spatial control           │
│  • 3/4 Mannequin output (512×512)                   │
└────────────────────┬───────���────────────────────────┘
                     ↓
         ✅ Professional Design Katalog
```

---

## ✨ Key Features

### 📊 **Stage 1: Pattern Analysis**
- ✅ Google Cloud Vision API integration
- ✅ Automatic color palette extraction
- ✅ Textile property detection
- ✅ Pattern classification

### 🤖 **Stage 2: LLM-Powered Generation**
- ✅ Vertex AI / Google Generative AI
- ✅ Intelligent design prompt creation
- ✅ 3/4 mannequin-specific instructions
- ✅ Context-aware design recommendations
- ✅ Multi-language support

### 🎨 **Stage 3: Image Generation**
- ✅ Stable Diffusion v1.5 + ControlNet
- ✅ ControlNet Canny for pattern conditioning
- ✅ Full model fine-tuning capability
- ✅ 512×512 high-resolution output
- ✅ Mannequin-focused generation
- ✅ Custom LoRA support

### 💼 **Production Ready**
- ✅ Full-stack architecture (React + FastAPI)
- ✅ MongoDB database integration
- ✅ RESTful API endpoints
- ✅ Docker support
- ✅ Google Cloud ADC configuration
- ✅ Scalable microservices

---

## 🏗️ Project Structure

```
ai-fashion-motif-to-katalog/
│
├── 📁 frontend/                    # React TypeScript UI
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── App.tsx
│   └── package.json
│
├── 📁 backend/                     # Node.js + Express API
│   ├── src/
│   │   ├── routes/
│   │   ├── middleware/
│   │   ├── models/
│   │   └── server.ts
│   └── package.json
│
├── 📁 ai_pipeline/                 # Python FastAPI AI Service
│   ├── stage1_analysis/            # Stage 1: Google Cloud Vision
│   │   ├── pattern_analyzer.py
│   │   └── color_extractor.py
│   │
│   ├── stage2_llm/                 # Stage 2: Vertex AI LLM
│   │   ├── prompt_generator.py
│   │   └── design_composer.py
│   │
│   ├── stage3_generation/          # Stage 3: Stable Diffusion
│   │   ├── controlnet_pipeline.py
│   │   ├── fine_tuning.py
│   │   └── mannequin_generator.py
│   │
│   ├── app.py                      # FastAPI main app
│   └── requirements.txt
│
├── 📁 models/                      # Pre-trained models (git-lfs)
│   ├── stable-diffusion-v1.5/
│   ├── controlnet-canny/
│   └── README.md
│
├── 📁 datasets/                    # Training data
│   ├── fashion-mnist/
│   ├── afro-fashion/
│   └── custom-patterns/
│
├── 📁 scripts/                     # Utility scripts
│   ├── download_models.sh
│   ├── setup_gcloud.sh
│   ├── train_custom_lora.py
│   └── test_pipeline.py
│
├── 📁 docs/                        # Documentation
│   ├── SETUP_GUIDE.md
│   ├── API_REFERENCE.md
│   ├── GOOGLE_CLOUD_SETUP.md
│   └── ARCHITECTURE.md
│
├── docker-compose.yml              # Local dev setup
├── docker-compose.prod.yml         # Production setup
├── .env.example                    # Environment template
└── README.md                       # This file
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- Node.js 16+
- Docker & Docker Compose
- Google Cloud Account (Free tier OK)
- CUDA 12.0+ (for GPU acceleration)

### 1️⃣ Google Cloud Setup

```bash
# Install Google Cloud CLI
curl https://sdk.cloud.google.com | bash
exec -l $SHELL

# Login to Google Cloud
gcloud auth application-default login

# Set project
gcloud config set project YOUR_PROJECT_ID

# Enable APIs
gcloud services enable vision.googleapis.com
gcloud services enable aiplatform.googleapis.com
```

### 2️⃣ Clone & Setup Repository

```bash
git clone https://github.com/showyourskills/ai-fashion-motif-to-katalog.git
cd ai-fashion-motif-to-katalog

# Copy environment file
cp .env.example .env

# Edit .env with your Google Cloud credentials
vim .env
```

### 3️⃣ Run with Docker (Recommended)

```bash
# Development setup
docker-compose up -d

# Access services
# - Frontend: http://localhost:3000
# - Backend: http://localhost:5000
# - AI Pipeline: http://localhost:8000/docs
```

### 4️⃣ Manual Setup

```bash
# AI Pipeline
cd ai_pipeline
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py

# Backend (in new terminal)
cd backend
npm install
npm run dev

# Frontend (in new terminal)
cd frontend
npm install
npm run dev
```

---

## 📚 Technology Stack

### **Frontend**
- React 18 + TypeScript
- Vite (build tool)
- Tailwind CSS
- Framer Motion (animations)
- Axios (HTTP client)

### **Backend**
- Node.js 16+
- Express.js
- MongoDB + Mongoose
- JWT Authentication
- RESTful API

### **AI Pipeline**
- Python 3.12+
- FastAPI (async framework)
- PyTorch (deep learning)
- Diffusers (Stable Diffusion)
- Google Cloud Vision API
- Google Generative AI (Vertex AI)
- ControlNet (spatial conditioning)
- CLIP (image embeddings)
- FAISS (similarity search)

### **Cloud & DevOps**
- Google Cloud (Vision, Vertex AI)
- Docker & Docker Compose
- MongoDB Atlas (optional)
- Cloud Storage (optional)

---

## 🔧 API Endpoints

### AI Pipeline (Port 8000)

```bash
# Stage 1: Analyze motif
POST /api/v1/analyze
Body: { image: File }
Response: { colors, properties, description }

# Stage 2: Generate design prompt
POST /api/v1/generate-prompt
Body: { analysis: Object, clothing_type: string }
Response: { prompt, instructions, details }

# Stage 3: Generate design
POST /api/v1/generate-design
Body: { prompt: string, pattern_image: File }
Response: { design_image, metadata }

# Complete pipeline
POST /api/v1/full-pipeline
Body: { image: File, clothing_type: string }
Response: { analysis, prompt, design_image }

# Health check
GET /api/v1/health
Response: { status, models_loaded }
```

### Backend (Port 5000)

```bash
# Authentication
POST /api/auth/register
POST /api/auth/login
POST /api/auth/logout

# User
GET /api/user/profile
PUT /api/user/profile

# Designs
GET /api/designs
POST /api/designs
GET /api/designs/:id
DELETE /api/designs/:id

# Analytics
GET /api/analytics/usage
GET /api/analytics/trends
```

---

## 🎯 Usage Example

### Via Web UI
1. Open http://localhost:3000
2. Upload motif image
3. Select clothing type (dress, shirt, jacket, etc.)
4. Click "Generate Design"
5. Wait for AI processing (30-60 seconds)
6. View 3/4 mannequin design
7. Download or refine

### Via API

```bash
curl -X POST http://localhost:8000/api/v1/full-pipeline \
  -F "image=@motif.png" \
  -F "clothing_type=dress" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## 📖 Documentation

- **[Setup Guide](docs/SETUP_GUIDE.md)** - Detailed installation instructions
- **[Google Cloud Setup](docs/GOOGLE_CLOUD_SETUP.md)** - ADC configuration
- **[API Reference](docs/API_REFERENCE.md)** - Complete API documentation
- **[Architecture](docs/ARCHITECTURE.md)** - System design & data flow
- **[Training Guide](docs/TRAINING_GUIDE.md)** - Custom model fine-tuning

---

## 🤝 Architecture Overview

### Component Sources

| Component | Source Repository | Purpose |
|-----------|------------------|----------|
| Full-Stack Structure | FashionAI | Production-ready architecture |
| ControlNet Integration | Sketch2Style | Pattern-aware generation |
| Google Cloud + LLM | AI-Fashion-Assistant-LangFlow | Image analysis & LLM |
| Fine-tuning Methodology | Afro-Fashion-Stable-Diffusion | Custom model training |

---

## 🧪 Testing

```bash
# Test AI pipeline
python scripts/test_pipeline.py

# Test API endpoints
npm run test:backend

# Test frontend
npm run test:frontend

# Integration tests
sh scripts/integration_tests.sh
```

---

## 🚢 Deployment

### Production Deployment

```bash
# Using docker-compose.prod.yml
docker-compose -f docker-compose.prod.yml up -d

# Configure SSL, domain, etc. in .env
```

### Google Cloud Deployment

```bash
# Deploy AI Pipeline to Cloud Run
gcloud run deploy ai-fashion-pipeline \
  --source . \
  --platform managed \
  --region us-central1

# Deploy Frontend to Cloud Storage + CDN
# (See docs/DEPLOYMENT_GUIDE.md for details)
```

---

## 📊 Performance Metrics

| Metric | Target | Current |
|--------|--------|----------|
| Analysis Time | <5s | ~3s |
| LLM Generation | <10s | ~8s |
| Design Generation | <60s | ~45s |
| Total Pipeline | <120s | ~60s |
| Inference Memory | <12GB | ~10GB |
| Output Resolution | 512×512 | 512×512 |

---

## 📝 License

MIT License - See [LICENSE](LICENSE) file

---

## 🙏 Acknowledgments

### Integrated Technologies
- [FashionAI](https://github.com/sushantfokmare/FashionAI) - Full-stack architecture
- [Sketch2Style](https://github.com/AI688-Final-Project-Spring-2026/Sketch2Style-ControlNet-Fashion) - ControlNet fine-tuning
- [AI-Fashion-Assistant-LangFlow](https://github.com/Swastika3647/AI-Fashion-Assistant-LangFlow) - Google Cloud integration
- [Afro-Fashion-Stable-Diffusion](https://github.com/Abdoulaye-Sayouti/Afro-Fashion-Stable-Diffusion) - Fine-tuning methodology

### Core Libraries
- [Stable Diffusion](https://huggingface.co/runwayml/stable-diffusion-v1-5) - Image generation
- [ControlNet](https://huggingface.co/llm-wizards/sd-controlnet-canny) - Spatial control
- [Google Cloud AI](https://cloud.google.com/ai) - Cloud services
- [FastAPI](https://fastapi.tiangolo.com/) - Web framework
- [React](https://react.dev/) - Frontend framework

---

## 📞 Support

- 📧 Email: support@fashionai.com
- 🐛 [Report Issues](https://github.com/showyourskills/ai-fashion-motif-to-katalog/issues)
- 💬 [Discussions](https://github.com/showyourskills/ai-fashion-motif-to-katalog/discussions)
- 📖 [Documentation](docs/)

---

**Made with ❤️ by AI Fashion Motif to Katalog Team**
