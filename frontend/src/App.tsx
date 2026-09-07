import React, { useState, useEffect, useRef } from 'react';

interface DominantColor {
  hex: string;
  rgb: number[];
  percentage: number;
}

interface AnalysisData {
  dimensions: { width: number; height: number };
  format: string;
  colors: DominantColor[];
  dominant_color: string;
  labels: string[];
  properties: string;
  auth_mode?: string;
  description: string;
}

interface PromptData {
  prompt: string;
  negative_prompt: string;
  clothing_type: string;
  dominant_colors: string[];
  target_pose: string;
  engine: string;
}

interface CatalogData {
  image_base64: string;
  width: number;
  height: number;
  format: string;
  inference_time_seconds: number;
  engine: string;
  auth_mode?: string;
  metadata?: {
    prompt: string;
    negative_prompt: string;
    view: string;
  };
}

interface FullPipelineResponse {
  success: boolean;
  stage1_analysis: AnalysisData;
  stage2_prompt: PromptData;
  stage3_catalog: CatalogData;
}

const CLOTHING_OPTIONS = [
  'Batik Blazer',
  'Modern Dress',
  'Kebaya Modern',
  'Executive Shirt',
  'Evening Gown',
  'Casual Jacket'
];

const STYLE_OPTIONS = [
  'Modern Elegant Luxury',
  'Haute Couture Studio',
  'Minimalist Contemporary',
  'Heritage Traditional'
];

export const App: React.FC = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [clothingType, setClothingType] = useState<string>('Batik Blazer');
  const [customClothing, setCustomClothing] = useState<string>('');
  const [stylePreference, setStylePreference] = useState<string>('Modern Elegant Luxury');
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [elapsedSeconds, setElapsedSeconds] = useState<number>(0);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [result, setResult] = useState<FullPipelineResponse | null>(null);
  const [apiHealth, setApiHealth] = useState<'connected' | 'checking' | 'offline'>('checking');
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Check API health on load
  useEffect(() => {
    checkHealth();
  }, []);

  // Timer counter during generation
  useEffect(() => {
    let interval: any;
    if (isLoading) {
      interval = setInterval(() => {
        setElapsedSeconds((prev) => prev + 1);
      }, 1000);
    } else {
      setElapsedSeconds(0);
    }
    return () => clearInterval(interval);
  }, [isLoading]);

  const checkHealth = async () => {
    try {
      setApiHealth('checking');
      const res = await fetch('http://localhost:8000/api/v1/health');
      if (res.ok) {
        setApiHealth('connected');
      } else {
        setApiHealth('offline');
      }
    } catch {
      setApiHealth('offline');
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      setSelectedFile(file);
      setPreviewUrl(URL.createObjectURL(file));
      setErrorMessage(null);
    }
  };

  // Helper untuk membuat sampel motif batik via Canvas (memudahkan tes instan)
  const generateSamplePattern = () => {
    const canvas = document.createElement('canvas');
    canvas.width = 300;
    canvas.height = 300;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // Gradien dasar kain
    const grad = ctx.createLinearGradient(0, 0, 300, 300);
    grad.addColorStop(0, '#781d1d');
    grad.addColorStop(0.5, '#c27803');
    grad.addColorStop(1, '#1e3a8a');
    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, 300, 300);

    // Pola ornamen geometris batik
    ctx.strokeStyle = '#fef08a';
    ctx.lineWidth = 3;
    for (let x = 30; x < 300; x += 60) {
      for (let y = 30; y < 300; y += 60) {
        ctx.beginPath();
        ctx.arc(x, y, 20, 0, Math.PI * 2);
        ctx.stroke();
        ctx.beginPath();
        ctx.arc(x, y, 8, 0, Math.PI * 2);
        ctx.fillStyle = '#fde047';
        ctx.fill();
      }
    }

    canvas.toBlob((blob) => {
      if (blob) {
        const file = new File([blob], 'sample_batik_motif.png', { type: 'image/png' });
        setSelectedFile(file);
        setPreviewUrl(URL.createObjectURL(blob));
        setErrorMessage(null);
      }
    }, 'image/png');
  };

  const handleGenerate = async () => {
    if (!selectedFile) {
      setErrorMessage('Silakan unggah atau buat sampel gambar motif terlebih dahulu.');
      return;
    }

    setIsLoading(true);
    setErrorMessage(null);

    const formData = new FormData();
    formData.append('file', selectedFile);
    formData.append('clothing_type', customClothing.trim() || clothingType);
    formData.append('style', stylePreference);

    try {
      const response = await fetch('http://localhost:8000/api/v1/full-pipeline', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errJson = await response.json().catch(() => ({}));
        throw new Error(errJson.detail || `Server error (${response.status})`);
      }

      const data: FullPipelineResponse = await response.json();
      setResult(data);
    } catch (err: any) {
      setErrorMessage(err.message || 'Gagal memproses pipeline. Pastikan API server aktif.');
    } finally {
      setIsLoading(false);
    }
  };

  const downloadCatalogImage = () => {
    if (!result?.stage3_catalog?.image_base64) return;
    const link = document.createElement('a');
    link.href = `data:image/png;base64,${result.stage3_catalog.image_base64}`;
    link.download = `katalog_3_4_${(customClothing || clothingType).toLowerCase().replace(/\s+/g, '_')}.png`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div style={{ maxWidth: 1380, margin: '0 auto', padding: '32px 24px' }}>
      {/* HEADER */}
      <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 36 }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
            <span style={{ fontSize: 32 }}>🎨</span>
            <h1 style={{ fontSize: 26, fontWeight: 800, letterSpacing: '-0.5px' }}>
              AI Fashion Motif <span style={{ color: 'var(--accent-blue)' }}>to Katalog</span>
            </h1>
          </div>
          <p style={{ color: 'var(--text-muted)', fontSize: 14, marginTop: 4 }}>
            100% Cloud-Powered AI • Google Cloud ADC (Vision API + Vertex AI Gemini + Google Imagen 3)
          </p>
        </div>

        {/* HEALTH STATUS PILL */}
        <div
          onClick={checkHealth}
          title="Klik untuk cek ulang koneksi API"
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: 8,
            padding: '8px 16px',
            borderRadius: 999,
            backgroundColor: 'rgba(255,255,255,0.05)',
            border: '1px solid var(--border-color)',
            fontSize: 13,
            cursor: 'pointer'
          }}
        >
          <span
            style={{
              width: 8,
              height: 8,
              borderRadius: '50%',
              backgroundColor: apiHealth === 'connected' ? '#22c55e' : apiHealth === 'checking' ? '#eab308' : '#ef4444'
            }}
          />
          <span style={{ color: apiHealth === 'connected' ? '#86efac' : '#cbd5e1' }}>
            {apiHealth === 'connected' ? 'API Siap (Port 8000)' : apiHealth === 'checking' ? 'Memeriksa API...' : 'API Offline'}
          </span>
        </div>
      </header>

      {/* ERROR BANNER */}
      {errorMessage && (
        <div
          style={{
            backgroundColor: 'rgba(239, 68, 68, 0.15)',
            border: '1px solid rgba(239, 68, 68, 0.4)',
            color: '#fca5a5',
            padding: '12px 18px',
            borderRadius: 12,
            marginBottom: 24,
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center'
          }}
        >
          <span>⚠️ {errorMessage}</span>
          <button
            onClick={() => setErrorMessage(null)}
            style={{ background: 'transparent', color: '#fca5a5', fontSize: 16 }}
          >
            ✕
          </button>
        </div>
      )}

      {/* MAIN GRID LAYOUT */}
      <div style={{ display: 'grid', gridTemplateColumns: '460px 1fr', gap: 32, alignItems: 'start' }}>
        
        {/* LEFT COLUMN: INPUT CONTROLS */}
        <div
          style={{
            backgroundColor: 'var(--bg-card)',
            backdropFilter: 'blur(12px)',
            borderRadius: 20,
            border: '1px solid var(--border-color)',
            padding: 24,
            display: 'flex',
            flexDirection: 'column',
            gap: 24
          }}
        >
          {/* UPLOAD MOTIF SECTION */}
          <div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 12 }}>
              <label style={{ fontSize: 14, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.5 }}>
                1. Unggah Gambar Motif
              </label>
              <button
                type="button"
                onClick={generateSamplePattern}
                style={{
                  background: 'rgba(56, 189, 248, 0.15)',
                  color: 'var(--accent-blue)',
                  padding: '4px 10px',
                  borderRadius: 6,
                  fontSize: 12,
                  fontWeight: 600
                }}
              >
                + Sampel Motif
              </button>
            </div>

            <input
              type="file"
              ref={fileInputRef}
              onChange={handleFileChange}
              accept="image/*"
              style={{ display: 'none' }}
            />

            {!previewUrl ? (
              <div
                onClick={() => fileInputRef.current?.click()}
                style={{
                  border: '2px dashed rgba(255,255,255,0.15)',
                  borderRadius: 14,
                  padding: '40px 20px',
                  textAlign: 'center',
                  cursor: 'pointer',
                  backgroundColor: 'rgba(0,0,0,0.2)',
                  transition: 'all 0.2s'
                }}
              >
                <div style={{ fontSize: 36, marginBottom: 8 }}>🖼️</div>
                <div style={{ fontSize: 14, fontWeight: 600 }}>Klik untuk pilih file motif</div>
                <div style={{ fontSize: 12, color: 'var(--text-muted)', marginTop: 4 }}>
                  Mendukung PNG, JPEG, WebP (Maks 15MB)
                </div>
              </div>
            ) : (
              <div style={{ position: 'relative', borderRadius: 14, overflow: 'hidden', border: '1px solid var(--border-color)' }}>
                <img
                  src={previewUrl}
                  alt="Motif preview"
                  style={{ width: '100%', height: 220, objectFit: 'cover', display: 'block' }}
                />
                <div
                  style={{
                    position: 'absolute',
                    top: 8,
                    right: 8,
                    display: 'flex',
                    gap: 6
                  }}
                >
                  <button
                    onClick={() => fileInputRef.current?.click()}
                    style={{
                      backgroundColor: 'rgba(0,0,0,0.7)',
                      color: '#fff',
                      padding: '4px 8px',
                      borderRadius: 6,
                      fontSize: 12
                    }}
                  >
                    Ganti
                  </button>
                  <button
                    onClick={() => {
                      setSelectedFile(null);
                      setPreviewUrl(null);
                    }}
                    style={{
                      backgroundColor: 'rgba(239,68,68,0.8)',
                      color: '#fff',
                      padding: '4px 8px',
                      borderRadius: 6,
                      fontSize: 12
                    }}
                  >
                    Hapus
                  </button>
                </div>
              </div>
            )}
          </div>

          {/* CLOTHING TYPE SELECTION */}
          <div>
            <label style={{ fontSize: 14, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.5, display: 'block', marginBottom: 12 }}>
              2. Jenis Busana Manekin
            </label>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: 8 }}>
              {CLOTHING_OPTIONS.map((item) => (
                <button
                  key={item}
                  type="button"
                  onClick={() => {
                    setClothingType(item);
                    setCustomClothing('');
                  }}
                  style={{
                    padding: '10px 12px',
                    borderRadius: 10,
                    fontSize: 13,
                    fontWeight: 600,
                    backgroundColor: clothingType === item && !customClothing ? 'var(--accent-blue)' : 'rgba(255,255,255,0.04)',
                    color: clothingType === item && !customClothing ? '#0b0f19' : 'var(--text-primary)',
                    border: '1px solid var(--border-color)',
                    textAlign: 'center'
                  }}
                >
                  {item}
                </button>
              ))}
            </div>
            <input
              type="text"
              placeholder="Atau ketik model busana kustom..."
              value={customClothing}
              onChange={(e) => setCustomClothing(e.target.value)}
              style={{
                width: '100%',
                marginTop: 10,
                padding: '10px 14px',
                borderRadius: 10,
                backgroundColor: 'rgba(0,0,0,0.3)',
                border: '1px solid var(--border-color)',
                color: '#fff',
                fontSize: 13
              }}
            />
          </div>

          {/* STYLE PREFERENCE */}
          <div>
            <label style={{ fontSize: 14, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.5, display: 'block', marginBottom: 12 }}>
              3. Preferensi Gaya & Tata Lampu
            </label>
            <select
              value={stylePreference}
              onChange={(e) => setStylePreference(e.target.value)}
              style={{
                width: '100%',
                padding: '12px 14px',
                borderRadius: 10,
                backgroundColor: 'rgba(0,0,0,0.4)',
                border: '1px solid var(--border-color)',
                color: '#fff',
                fontSize: 13
              }}
            >
              {STYLE_OPTIONS.map((opt) => (
                <option key={opt} value={opt} style={{ background: '#131b2e' }}>
                  {opt}
                </option>
              ))}
            </select>
          </div>

          {/* SUBMIT BUTTON */}
          <button
            type="button"
            disabled={isLoading || !selectedFile}
            onClick={handleGenerate}
            style={{
              padding: '16px 20px',
              borderRadius: 14,
              fontSize: 15,
              fontWeight: 700,
              background: isLoading || !selectedFile ? 'rgba(255,255,255,0.1)' : 'linear-gradient(135deg, #38bdf8 0%, #2563eb 100%)',
              color: isLoading || !selectedFile ? 'var(--text-muted)' : '#ffffff',
              boxShadow: isLoading || !selectedFile ? 'none' : '0 10px 25px -5px rgba(37, 99, 235, 0.4)',
              cursor: isLoading || !selectedFile ? 'not-allowed' : 'pointer'
            }}
          >
            {isLoading ? `Sedang Memproses... (${elapsedSeconds}s)` : '✨ Hasilkan Katalog Manekin 3/4'}
          </button>
        </div>

        {/* RIGHT COLUMN: 3-STAGE RESULTS */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: 24 }}>
          {!result ? (
            <div
              style={{
                backgroundColor: 'var(--bg-card)',
                borderRadius: 20,
                border: '1px solid var(--border-color)',
                padding: '80px 40px',
                textAlign: 'center',
                color: 'var(--text-muted)'
              }}
            >
              <div style={{ fontSize: 48, marginBottom: 16 }}>👘</div>
              <h3 style={{ fontSize: 20, color: '#f1f5f9', fontWeight: 700, marginBottom: 8 }}>
                Katalog Belum Dihasilkan
              </h3>
              <p style={{ maxWidth: 460, margin: '0 auto', fontSize: 14, lineHeight: 1.6 }}>
                Pilih atau buat sampel motif di panel kiri, tentukan jenis pakaian, lalu klik tombol untuk mengeksekusi pipeline 3-Stage Google Cloud.
              </p>
            </div>
          ) : (
            <>
              {/* STAGE 3: CATALOG MANNEQUIN IMAGE RESULT (HERO) */}
              <div
                style={{
                  backgroundColor: 'var(--bg-card)',
                  borderRadius: 20,
                  border: '1px solid var(--border-color)',
                  padding: 24,
                  display: 'flex',
                  flexDirection: 'column',
                  gap: 20
                }}
              >
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <div>
                    <span style={{ fontSize: 12, fontWeight: 700, color: 'var(--accent-gold)', letterSpacing: 1 }}>
                      STAGE 3 • GENERASI CITRA
                    </span>
                    <h2 style={{ fontSize: 22, fontWeight: 800, marginTop: 4 }}>
                      Hasil Katalog Manekin 3/4
                    </h2>
                  </div>
                  <div style={{ display: 'flex', gap: 10 }}>
                    <span
                      style={{
                        padding: '6px 12px',
                        borderRadius: 8,
                        backgroundColor: 'rgba(255,255,255,0.06)',
                        fontSize: 12,
                        color: 'var(--text-muted)'
                      }}
                    >
                      ⚡ {result.stage3_catalog.inference_time_seconds}s
                    </span>
                    <button
                      type="button"
                      onClick={downloadCatalogImage}
                      style={{
                        padding: '8px 16px',
                        borderRadius: 10,
                        backgroundColor: 'var(--accent-blue)',
                        color: '#0b0f19',
                        fontSize: 13,
                        fontWeight: 700
                      }}
                    >
                      ⬇ Unduh Gambar
                    </button>
                  </div>
                </div>

                <div style={{ display: 'flex', justifyContent: 'center', backgroundColor: '#000', borderRadius: 14, padding: 16 }}>
                  <img
                    src={`data:image/png;base64,${result.stage3_catalog.image_base64}`}
                    alt="Hasil Katalog 3/4 Manekin"
                    style={{
                      maxWidth: '100%',
                      maxHeight: 520,
                      borderRadius: 8,
                      boxShadow: '0 20px 25px -5px rgba(0,0,0,0.5)'
                    }}
                  />
                </div>

                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 12, color: 'var(--text-muted)' }}>
                  <span>Engine: <strong>{result.stage3_catalog.engine}</strong></span>
                  <span>Resolusi: {result.stage3_catalog.width} × {result.stage3_catalog.height} px</span>
                  <span>Sudut: 3/4 View Mannequin</span>
                </div>
              </div>

              {/* STAGE 1: PATTERN ANALYSIS CARD */}
              <div
                style={{
                  backgroundColor: 'var(--bg-card)',
                  borderRadius: 20,
                  border: '1px solid var(--border-color)',
                  padding: 24
                }}
              >
                <div style={{ marginBottom: 16 }}>
                  <span style={{ fontSize: 12, fontWeight: 700, color: 'var(--accent-blue)', letterSpacing: 1 }}>
                    STAGE 1 • ANALISIS GOOGLE CLOUD VISION
                  </span>
                  <h3 style={{ fontSize: 18, fontWeight: 700, marginTop: 4 }}>
                    Palet Warna & Karakteristik Tekstil
                  </h3>
                </div>

                {/* COLOR PALETTE CHIPS */}
                <div style={{ marginBottom: 16 }}>
                  <label style={{ fontSize: 12, color: 'var(--text-muted)', display: 'block', marginBottom: 8 }}>
                    Palet Warna Dominan
                  </label>
                  <div style={{ display: 'flex', gap: 12, flexWrap: 'wrap' }}>
                    {result.stage1_analysis.colors.map((c, idx) => (
                      <div
                        key={idx}
                        style={{
                          display: 'flex',
                          alignItems: 'center',
                          gap: 8,
                          backgroundColor: 'rgba(0,0,0,0.3)',
                          padding: '6px 12px',
                          borderRadius: 8,
                          border: '1px solid var(--border-color)'
                        }}
                      >
                        <span
                          style={{
                            width: 18,
                            height: 18,
                            borderRadius: 4,
                            backgroundColor: c.hex,
                            border: '1px solid rgba(255,255,255,0.2)'
                          }}
                        />
                        <span style={{ fontSize: 13, fontWeight: 600, fontFamily: 'monospace' }}>{c.hex}</span>
                        <span style={{ fontSize: 11, color: 'var(--text-muted)' }}>{c.percentage}%</span>
                      </div>
                    ))}
                  </div>
                </div>

                {/* TEXTILE LABELS */}
                <div>
                  <label style={{ fontSize: 12, color: 'var(--text-muted)', display: 'block', marginBottom: 6 }}>
                    Karakteristik & Label
                  </label>
                  <p style={{ fontSize: 13, color: '#e2e8f0' }}>{result.stage1_analysis.properties}</p>
                </div>
              </div>

              {/* STAGE 2: LLM PROMPT CARD */}
              <div
                style={{
                  backgroundColor: 'var(--bg-card)',
                  borderRadius: 20,
                  border: '1px solid var(--border-color)',
                  padding: 24
                }}
              >
                <div style={{ marginBottom: 14 }}>
                  <span style={{ fontSize: 12, fontWeight: 700, color: '#a855f7', letterSpacing: 1 }}>
                    STAGE 2 • GOOGLE VERTEX AI GEMINI
                  </span>
                  <h3 style={{ fontSize: 18, fontWeight: 700, marginTop: 4 }}>
                    Prompt Difusi Katalog Manekin 3/4
                  </h3>
                </div>

                <div
                  style={{
                    backgroundColor: 'rgba(0,0,0,0.4)',
                    padding: 14,
                    borderRadius: 10,
                    border: '1px solid var(--border-color)',
                    fontSize: 13,
                    lineHeight: 1.6,
                    color: '#cbd5e1'
                  }}
                >
                  <strong style={{ color: '#38bdf8' }}>Positive Prompt:</strong> {result.stage2_prompt.prompt}
                </div>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
};

export default App;
