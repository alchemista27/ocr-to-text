#!/usr/bin/env python3
"""
OCR Batch Processor dengan Resume Otomatis
- Membaca file PDF dari folder target
- Menggunakan EasyOCR
- Memproses 500 file per batch
- Menyimpan hasil di folder output
- Otomatis skip file yang sudah selesai (pakai log file)
"""

import os
from pdf2image import convert_from_path
import numpy as np
import cv2
import easyocr

# === Setting path input/output ===
INPUT_PATH = os.path.expanduser("~/local-drive/folder-target-pekerjaan")
OUTPUT_PATH = os.path.expanduser("~/local-drive/hasil-pekerjaan")
LOG_FILE = os.path.join(OUTPUT_PATH, "processed.log")

# Buat folder output jika belum ada
os.makedirs(OUTPUT_PATH, exist_ok=True)

# Ambil semua file di input
file_list = sorted(os.listdir(INPUT_PATH))
file_list = file_list[1:]  # skip index 0 kalau ada file aneh
print(f"Total file ditemukan: {len(file_list)}")

# === Fungsi preprocessing gambar ===
def preprocessing(img):
    gray = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 3)
    gray = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, 11, 2
    )
    return gray

# === Setup EasyOCR ===
reader = easyocr.Reader(['id', 'en'], gpu=False)

# === Baca file log kalau ada ===
if os.path.exists(LOG_FILE):
    with open(LOG_FILE, "r") as f:
        processed_files = set(line.strip() for line in f if line.strip())
else:
    processed_files = set()

print(f"File sudah diproses: {len(processed_files)}")

# === Parameter batch ===
batch_size = 500

# === Loop per batch ===
for batch_start in range(0, len(file_list), batch_size):
    batch_end = batch_start + batch_size
    batch_files = file_list[batch_start:batch_end]

    print(f"\n🔄 Memproses batch {batch_start} - {batch_end-1} "
          f"(total {len(batch_files)} file)")

    for f in batch_files:
        if f in processed_files:
            print(f"⏭️ Skip (sudah ada): {f}")
            continue

        file_name = os.path.join(INPUT_PATH, f)

        try:
            pages = convert_from_path(file_name, dpi=300)
            all_text = []

            # OCR per halaman
            for page in pages:
                img = preprocessing(page)
                result = reader.readtext(img, detail=0)

                text = " ".join(result)
                text = " ".join(text.split())
                all_text.append(text)

            # Simpan hasil ke .txt
            output_file = os.path.join(OUTPUT_PATH, f'{f[:-4]}.txt')
            with open(output_file, 'w', encoding='utf-8') as o:
                o.write("\n\n".join(all_text))

            # Tambahkan ke log
            with open(LOG_FILE, "a") as log:
                log.write(f + "\n")

            print(f"✅ Selesai: {f}")

        except Exception as e:
            print(f"❌ Error memproses {f}: {e}")