# Google Cloud Setup Guide

## Prerequisites

- Google Cloud Account (Free tier sufficient)
- `gcloud` CLI installed
- `gsutil` CLI installed
- Active internet connection

---

## Step 1: Create Google Cloud Project

### Via Console

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click on project dropdown → Select "New Project"
3. Enter project name: `ai-fashion-motif`
4. Click "Create"
5. Wait for creation to complete

### Via gcloud CLI

```bash
gcloud projects create ai-fashion-motif \
  --name="AI Fashion Motif Generator"

# Set as active project
gcloud config set project ai-fashion-motif
```

---

## Step 2: Enable Required APIs

```bash
# Vision API (for pattern analysis)
gcloud services enable vision.googleapis.com

# Vertex AI (for LLM)
gcloud services enable aiplatform.googleapis.com

# Compute Engine (for GPUs)
gcloud services enable compute.googleapis.com

# Cloud Run (for deployment)
gcloud services enable run.googleapis.com

# Cloud Storage (for file storage)
gcloud services enable storage-api.googleapis.com

# Cloud SQL (for optional database)
gcloud services enable sqladmin.googleapis.com
```

**Verify:**
```bash
gcloud services list --enabled | grep -E "vision|aiplatform|compute|run|storage"
```

---

## Step 3: Set up Authentication (ADC)

### Option A: Application Default Credentials (Easiest)

```bash
# Login with your Google account
gcloud auth application-default login

# This will:
# 1. Open browser for authentication
# 2. Save credentials to ~/.config/gcloud/application_default_credentials.json
# 3. Automatically used by Python libraries
```

**Verify:**
```bash
ls ~/.config/gcloud/application_default_credentials.json
echo $GOOGLE_APPLICATION_CREDENTIALS
```

### Option B: Service Account (For Production)

```bash
# Create service account
gcloud iam service-accounts create ai-fashion-sa \
  --display-name="AI Fashion Service Account"

# Grant permissions
gcloud projects add-iam-policy-binding ai-fashion-motif \
  --member=serviceAccount:ai-fashion-sa@ai-fashion-motif.iam.gserviceaccount.com \
  --role=roles/aiplatform.user

gcloud projects add-iam-policy-binding ai-fashion-motif \
  --member=serviceAccount:ai-fashion-sa@ai-fashion-motif.iam.gserviceaccount.com \
  --role=roles/storage.admin

gcloud projects add-iam-policy-binding ai-fashion-motif \
  --member=serviceAccount:ai-fashion-sa@ai-fashion-motif.iam.gserviceaccount.com \
  --role=roles/vision.client

# Create and download key
gcloud iam service-accounts keys create service-account-key.json \
  --iam-account=ai-fashion-sa@ai-fashion-motif.iam.gserviceaccount.com

# Set environment variable
export GOOGLE_APPLICATION_CREDENTIALS=$(pwd)/service-account-key.json
```

---

## Step 4: Create Cloud Storage Bucket

```bash
# Create bucket for images
gsutil mb gs://ai-fashion-motif-images

# Set lifecycle policy (optional - delete after 30 days)
cat > lifecycle.json << EOF
{
  "lifecycle": {
    "rule": [
      {
        "action": {"type": "Delete"},
        "condition": {"age": 30}
      }
    ]
  }
}
EOF

gsutil lifecycle set lifecycle.json gs://ai-fashion-motif-images

# Set permissions
gsutil iam ch serviceAccount:ai-fashion-sa@ai-fashion-motif.iam.gserviceaccount.com:objectCreator \
  gs://ai-fashion-motif-images
```

---

## Step 5: Configure Vertex AI

```bash
# Initialize Vertex AI (creates default bucket)
gcloud ai-platform models list

# Verify default region
gcloud config get-value compute/region

# Set default region (recommended: us-central1)
gcloud config set compute/region us-central1
```

---

## Step 6: Test Google Cloud Setup

### Test Vision API

```python
# test_vision.py
from google.cloud import vision

client = vision.ImageAnnotatorClient()
image = vision.Image(uri="gs://cloud-samples-data/vision/label/wakeup.jpg")
response = client.label_detection(image=image)
print("Labels:")
for label in response.label_annotations:
    print(f" {label.description}: {label.score:.2%}")
```

```bash
python test_vision.py
```

### Test Vertex AI

```python
# test_vertex_ai.py
import vertexai
from vertexai.language_models import TextGenerationModel

vertexai.init(project="ai-fashion-motif", location="us-central1")

model = TextGenerationModel.from_pretrained("text-bison@002")
response = model.predict(
    "What is fashion design?",
    temperature=0.2,
    max_output_tokens=100,
)
print(response.text)
```

```bash
python test_vertex_ai.py
```

### Test Cloud Storage

```python
# test_storage.py
from google.cloud import storage

client = storage.Client(project="ai-fashion-motif")
bucket = client.bucket("ai-fashion-motif-images")

# Test upload
blob = bucket.blob("test.txt")
blob.upload_from_string("Hello, World!")
print(f"Uploaded to gs://ai-fashion-motif-images/test.txt")

# Test download
blob = bucket.blob("test.txt")
print(blob.download_as_text())
```

```bash
python test_storage.py
```

---

## Step 7: Update .env File

```bash
# Copy from example
cp .env.example .env

# Edit .env
vim .env
```

```env
# Your actual Google Project ID
GOOGLE_PROJECT_ID=ai-fashion-motif

# Service account key (if using Option B)
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account-key.json

# Region (where your services are deployed)
VERTEX_AI_REGION=us-central1

# Bucket name
GCS_BUCKET_NAME=ai-fashion-motif-images
```

---

## Step 8: Verify Setup

```bash
# Check gcloud authentication
gcloud auth list

# Check active project
gcloud config list project

# Check enabled APIs
gcloud services list --enabled

# Check Cloud Storage buckets
gsutil ls

# Run test script
python scripts/test_google_cloud.py
```

**Expected Output:**
```
✅ Google Cloud Vision API: Connected
✅ Vertex AI / Generative AI: Connected  
✅ Cloud Storage: Connected
✅ All services operational
```

---

## Step 9: Set Billing (Free Tier)

1. Go to [Billing](https://console.cloud.google.com/billing)
2. Link billing account to project
3. Set up free tier alerts:
   - Click on "Budgets and alerts"
   - Create budget: $50/month
   - Get alerts when approaching limit

**Free Tier Includes:**
- Vision API: 1,000 requests/month
- Vertex AI: Limited inference
- Cloud Storage: 5GB/month
- Cloud Run: 180,000 GB-seconds/month

---

## Troubleshooting

### Error: "Permission denied"

```bash
# Check service account permissions
gcloud projects get-iam-policy ai-fashion-motif \
  --flatten="bindings[].members" \
  --filter="bindings.members:serviceAccount:*"

# Add missing permissions
gcloud projects add-iam-policy-binding ai-fashion-motif \
  --member=serviceAccount:ai-fashion-sa@ai-fashion-motif.iam.gserviceaccount.com \
  --role=roles/editor
```

### Error: "API not enabled"

```bash
# Enable specific API
gcloud services enable vision.googleapis.com

# Wait a few minutes for propagation
sleep 60

# Test again
python test_vision.py
```

### Error: "Invalid credentials"

```bash
# Re-authenticate
gcloud auth application-default login

# Or update credentials
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/new-key.json
```

---

## Next Steps

1. ✅ Google Cloud setup complete
2. → Run local development: `docker-compose up`
3. → Test full pipeline: `python scripts/test_pipeline.py`
4. → Deploy to Cloud Run: `gcloud run deploy ...`

---

## Additional Resources

- [Google Cloud Vision API Docs](https://cloud.google.com/vision/docs)
- [Vertex AI LLM Docs](https://cloud.google.com/vertex-ai/docs/generative-ai/model-reference/text)
- [Cloud Storage Docs](https://cloud.google.com/storage/docs)
- [gcloud CLI Reference](https://cloud.google.com/sdk/gcloud/reference)
