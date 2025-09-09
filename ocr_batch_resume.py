"""
OCR Batch Processor dengan Resume Otomatis (pakai pytesseract)
- Membaca file PDF dari folder target
- Menggunakan Tesseract OCR (CPU friendly)
- Memproses 500 file per batch
- Menyimpan hasil di folder output
- Otomatis skip file yang sudah selesai (pakai log file)
"""

import os
from pdf2image import convert_from_path
import pytesseract

# === Setting path input/output ===
INPUT_PATH = os.path.expanduser("~/local-drive/folder-target-pekerjaan")
OUTPUT_PATH = os.path.expanduser("~/local-drive/hasil-pekerjaan")
LOG_FILE = os.path.join(OUTPUT_PATH, "processed.log")

# Buat folder output kalau belum ada
os.makedirs(OUTPUT_PATH, exist_ok=True)

# Ambil semua file di input
file_list = sorted(os.listdir(INPUT_PATH))
file_list = file_list[1:]  # skip index 0 kalau ada file aneh
print(f"Total file ditemukan: {len(file_list)}")

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
            # Konversi PDF ke gambar (DPI 300 untuk OCR yang lebih akurat)
            pages = convert_from_path(file_name, dpi=300)
            all_text = []

            # OCR per halaman
            for page in pages:
                text = pytesseract.image_to_string(page, lang="ind+eng")
                text = " ".join(text.split())  # rapikan spasi
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