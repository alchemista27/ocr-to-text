"""
OCR Processor dengan Auto-Skip File Rusak (pakai pytesseract)
- Membaca file PDF dari folder target
- Hanya memproses file .pdf valid (skip ._xxx.pdf atau kosong)
- Tidak pakai looping batch, langsung cek per file
- Skip otomatis kalau file gagal dibaca (corrupt/bukan PDF)
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

# Ambil semua file PDF yang valid
file_list = sorted([
    f for f in os.listdir(INPUT_PATH)
    if f.lower().endswith(".pdf")
    and not f.startswith("._")  # skip file macOS resource fork
    and os.path.getsize(os.path.join(INPUT_PATH, f)) > 0  # skip file kosong
])

print(f"Total file PDF ditemukan: {len(file_list)}")

# === Loop per file ===
for f in file_list:
    file_name = os.path.join(INPUT_PATH, f)
    output_file = os.path.join(OUTPUT_PATH, f'{f[:-4]}.txt')

    # Skip kalau sudah ada hasilnya
    if os.path.exists(output_file):
        print(f"⏭️ Skip (sudah ada): {f}")
        continue

    print(f"\n🔄 Memproses file: {f}")

    try:
        # Konversi PDF ke gambar
        try:
            pages = convert_from_path(file_name, dpi=300)
        except Exception as e:
            print(f"⚠️ Skip {f} (bukan PDF valid / rusak): {e}")
            continue

        all_text = []

        # OCR per halaman
        for page in pages:
            text = pytesseract.image_to_string(page, lang="ind+eng")
            text = " ".join(text.split())  # rapikan spasi
            all_text.append(text)

        # Simpan hasil ke .txt
        with open(output_file, 'w', encoding='utf-8') as o:
            o.write("\n\n".join(all_text))

        print(f"✅ Selesai: {f}")

    except Exception as e:
        print(f"❌ Error memproses {f}: {e}")