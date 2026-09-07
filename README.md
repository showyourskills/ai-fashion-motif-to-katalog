# 🎨 AI Fashion Motif to Katalog Generator

> **100% Cloud-Powered AI Fashion Design System**  
> Transform motif patterns into professional 3/4 mannequin designs using Google Cloud AI (Vision API + Vertex AI Gemini + Google Imagen 3) via Application Default Credentials (ADC).

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Latest-009688.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18+-61DAFB.svg)](https://reactjs.org/)
[![Google Cloud](https://img.shields.io/badge/Google%20Cloud-ADC%20Ready-FF9800.svg)](https://cloud.google.com/)
[![Google Imagen 3](https://img.shields.io/badge/Google%20Imagen%203-Vertex%20AI-4285F4.svg)](https://cloud.google.com/vertex-ai)

---

## 🌟 Project Overview

Sistem ini dirancang 100% bertenaga cloud (*zero local hardware load*). Seluruh pemrosesan berat (analisis citra, reasoning LLM, dan perenderan gambar manekin katalog) dieksekusi langsung oleh infrastruktur Google Cloud melalui Application Default Credentials (ADC):

```
┌─────────────────────────────────────────────────────┐
│           Upload Motif/Pattern Image                │
└────────────────────┬────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────┐
│    STAGE 1: Google Cloud Vision API                 │
│  • Ekstraksi palet warna dominan (RGB & Hex)        │
│  • Deteksi karakteristik tekstil & pola busana      │
│  • Otentikasi otomatis via Google Cloud ADC         │
└────────────────────┬────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────┐
│  STAGE 2: Google Vertex AI (Gemini 1.5/2.0)         │
│  • Reasoning fashion designer & art director        │
│  • Formulasi prompt katalog manekin 3/4 profesional │
│  • Penataan drape kain, jahitan, & pencahayaan      │
└────────────────────┬────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────┐
│  STAGE 3: Google Vertex AI Imagen 3                 │
│  • Generasi foto katalog manekin 3/4 resolusi tinggi│
│  • Render studio minimalis tanpa beban GPU lokal    │
│  • Otentikasi mulus via Google Cloud ADC            │
└────────────────────┬────────────────────────────────┘
                     ↓
         ✅ Professional Design Katalog
```

---

## ✨ Fitur Utama

### 📊 **Stage 1: Analisis Motif (Google Cloud Vision)**
- ✅ Integrasi Google Cloud Vision API via ADC
- ✅ Ekstraksi otomatis palet warna dominan (Hex & RGB)
- ✅ Deteksi label material & tekstil kain
- ✅ Fallback lokal adaptif saat pengujian offline

### 🤖 **Stage 2: LLM Prompt Generator (Vertex AI Gemini)**
- ✅ Integrasi Google Vertex AI (Gemini) via ADC
- ✅ Prompt generator khusus **sudut pandang manekin 3/4 (3/4 mannequin view)**
- ✅ Negative prompt standar pemotretan katalog profesional
- ✅ Rekomendasi gaya busana kontekstual (blazer, dress, kebaya, kemeja)

### 🎨 **Stage 3: Generasi Desain Katalog (Google Imagen 3)**
- ✅ Bertenaga Google Cloud Imagen 3 (model generasi citra tercanggih dari Google)
- ✅ **100% Bebas Beban Hardware:** Tidak membutuhkan GPU NVIDIA, CUDA, atau VRAM besar di komputer Anda
- ✅ Output citra studio foto tajam dan beresolusi tinggi
- ✅ Ringan dan sangat cepat di-deploy ke Cloud Run

---

## 🏗️ Struktur Proyek

```
ai-fashion-motif-to-katalog/
│
├── 📁 frontend/                    # Antarmuka Pengguna (React + TypeScript)
├── 📁 backend/                     # API Gateway (Node.js / Express)
│
├── 📁 ai_pipeline/                 # Python FastAPI AI Service (Google Cloud)
│   ├── stage1_analysis/            # Stage 1: Google Cloud Vision (ADC)
│   │   ├── pattern_analyzer.py
│   │   └── __init__.py
│   │
│   ├── stage2_llm/                 # Stage 2: Vertex AI Gemini (ADC)
│   │   ├── prompt_generator.py
│   │   └── __init__.py
│   │
│   ├── stage3_generation/          # Stage 3: Google Vertex AI Imagen 3 (ADC)
│   │   ├── mannequin_generator.py
│   │   └── __init__.py
│   │
│   ├── tests/                      # Automated Unit & Integration Tests
│   │   └── test_pipeline.py
│   │
│   ├── app.py                      # FastAPI Main Server & Swagger UI
│   ├── Dockerfile                  # Container Deployment
│   └── requirements.txt            # Dependensi Python minimal & modern
│
├── 📁 scripts/                     # Skrip Otomasi & Pengujian CLI
│   └── test_pipeline.py            # Runner pengujian pipeline dari terminal
│
├── 📁 docs/                        # Dokumentasi Sistem
│   ├── GOOGLE_CLOUD_SETUP.md       # Panduan konfigurasi Google Cloud ADC
│   └── ARCHITECTURE.md             # Blueprint arsitektur cloud
│
├── docker-compose.yml              # Konfigurasi container lokal
├── .env.example                    # Template variabel lingkungan
└── README.md
```

---

## 🚀 Panduan Memulai Cepat

### Prasyarat
- Python 3.11+
- Akun Google Cloud dengan tagihan aktif (Free Tier tersedia kuota gratis)
- **Tidak memerlukan kartu grafis / GPU khusus** (cukup laptop atau komputer biasa)

### 1️⃣ Konfigurasi Google Cloud ADC

```bash
# 1. Login ke Google Cloud menggunakan Application Default Credentials (ADC)
gcloud auth application-default login

# 2. Set project ID Anda
gcloud config set project ID_PROJECT_ANDA

# 3. Aktifkan API yang dibutuhkan
gcloud services enable vision.googleapis.com
gcloud services enable aiplatform.googleapis.com
```

### 2️⃣ Menjalankan AI Pipeline Lokal

```bash
# Buat dan aktifkan virtual environment
uv venv .venv
.venv\Scripts\activate   # (di Windows)

# Pasang dependensi
uv pip install -r ai_pipeline/requirements.txt

# Jalankan server FastAPI
uvicorn ai_pipeline.app:app --reload --port 8000
```
Buka Swagger UI di browser: `http://localhost:8000/docs`

### 3️⃣ Uji Coba Langsung via Terminal (CLI)

```bash
python scripts/test_pipeline.py
```

---

## 🔧 Endpoint API (Port 8000)

| Method | Endpoint | Fungsi |
|---|---|---|
| `GET` | `/api/v1/health` | Status kesiapan seluruh stage AI |
| `POST` | `/api/v1/analyze` | Stage 1: Ekstraksi warna & karakteristik motif |
| `POST` | `/api/v1/generate-prompt` | Stage 2: Susun prompt katalog manekin 3/4 via Gemini |
| `POST` | `/api/v1/generate-design` | Stage 3: Generasi citra via Google Imagen 3 |
| `POST` | `/api/v1/full-pipeline` | Eksekusi lengkap (Motif $\rightarrow$ Analisis $\rightarrow$ Prompt $\rightarrow$ Katalog) |

---

## 📝 Lisensi
MIT License.
