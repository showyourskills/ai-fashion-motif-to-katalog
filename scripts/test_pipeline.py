"""
CLI Test Runner untuk AI Fashion Pipeline
Memungkinkan pengujian cepat dari terminal menggunakan gambar motif nyata atau dummy.
Penggunaan:
    python scripts/test_pipeline.py [path_ke_gambar_motif.jpg] [clothing_type]
"""

import sys
import os
import io

# Pastikan encoding stdout mendukung karakter beragam pada Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from PIL import Image, ImageDraw

# Tambahkan root proyek ke sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ai_pipeline.stage1_analysis.pattern_analyzer import PatternAnalyzer
from ai_pipeline.stage2_llm.prompt_generator import PromptGenerator
from ai_pipeline.stage3_generation.mannequin_generator import MannequinGenerator


def run_test():
    image_path = sys.argv[1] if len(sys.argv) > 1 else None
    clothing_type = sys.argv[2] if len(sys.argv) > 2 else "batik blazer"

    print("==================================================")
    print(" [AI FASHION MOTIF TO KATALOG] - TEST RUNNER")
    print("==================================================")

    if image_path and os.path.exists(image_path):
        print(f"[*] Membaca file motif: {image_path}")
        with open(image_path, "rb") as f:
            image_bytes = f.read()
    else:
        print("[*] Menggunakan citra motif sintetis (default test)...")
        img = Image.new("RGB", (256, 256), color=(140, 40, 40))
        draw = ImageDraw.Draw(img)
        draw.rectangle([60, 60, 196, 196], fill=(40, 100, 180))
        draw.ellipse([80, 80, 176, 176], fill=(240, 190, 70))
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        image_bytes = buf.getvalue()

    # Stage 1: Analisis Motif
    print("\n[STAGE 1] Menganalisis motif dan warna...")
    analyzer = PatternAnalyzer()
    analysis = analyzer.analyze_image_bytes(image_bytes)
    print(f"  + Warna Dominan : {analysis['dominant_color']}")
    print(f"  + Palet Warna   : {[c['hex'] for c in analysis['colors']]}")
    print(f"  + Karakteristik : {analysis['properties']}")
    print(f"  + Mode Auth     : {analysis.get('auth_mode', 'N/A')}")

    # Stage 2: Susun Prompt Busana
    print(f"\n[STAGE 2] Membuat prompt katalog manekin 3/4 untuk '{clothing_type}'...")
    prompt_gen = PromptGenerator()
    prompt_res = prompt_gen.generate_fashion_prompt(
        analysis=analysis,
        clothing_type=clothing_type,
        style_preference="modern elegant luxury"
    )
    print(f"  + Positive Prompt : {prompt_res['prompt']}")
    print(f"  + Engine Digunakan: {prompt_res['engine']}")

    # Stage 3: Render Citra Katalog
    print("\n[STAGE 3] Merender citra katalog manekin 3/4...")
    generator = MannequinGenerator()
    motif_pil = Image.open(io.BytesIO(image_bytes))
    design = generator.generate_design(
        prompt=prompt_res["prompt"],
        negative_prompt=prompt_res["negative_prompt"],
        pattern_image=motif_pil,
        width=512,
        height=512
    )

    out_file = "output_katalog_test.png"
    import base64
    with open(out_file, "wb") as f:
        f.write(base64.b64decode(design["image_base64"]))

    print(f"  + Waktu Render    : {design['inference_time_seconds']} detik")
    print(f"  + Engine Generasi : {design['engine']}")
    print(f"  + File Disimpan   : {out_file} (512x512 PNG)")
    print("\n[V] SELURUH TAHAP PIPELINE BERHASIL DIEKSEKUSI DENGAN SUKSES!")
    print("==================================================")


if __name__ == "__main__":
    run_test()
