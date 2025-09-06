# OCR Batch Processor with Resume

This project provides a batch processor for Optical Character Recognition (OCR) on scanned PDF files using EasyOCR. It is designed to efficiently process large numbers of files (e.g., 79,000+), with automatic batching, preprocessing, and resume capability.

## Features

- Reads PDF files from a target folder.
- Converts PDF pages to images and preprocesses them for better OCR accuracy.
- Uses [EasyOCR](https://github.com/JaidedAI/EasyOCR) for text extraction (supports Indonesian and English).
- Processes files in batches (default: 500 files per batch).
- Saves extracted text to `.txt` files in the output folder.
- Automatically skips files that have already been processed (using a log file).
- Robust error handling and progress reporting.

## Requirements

- Python 3.7+
- [pdf2image](https://pypi.org/project/pdf2image/)
- [numpy](https://numpy.org/)
- [opencv-python](https://pypi.org/project/opencv-python/)
- [easyocr](https://github.com/JaidedAI/EasyOCR)
- Poppler (for `pdf2image`)

## Installation

1. Install Python dependencies:
    ```sh
    pip install easyocr pdf2image numpy opencv-python
    ```

2. Install Poppler:
    - **Ubuntu:**  
      `sudo apt-get install poppler-utils`
    - **Windows:**  
      Download from [Poppler for Windows](http://blog.alivate.com.au/poppler-windows/), add to PATH.

## Usage

1. Place your PDF files in `~/local-drive/folder-target-pekerjaan`.
2. Run the batch processor:
    ```sh
    python ocr_batch_resume.py
    ```
3. Extracted text files will be saved in `~/local-drive/hasil-pekerjaan`.

The script will automatically resume from where it left off, skipping files already processed (tracked in `processed.log`).

## Customization

- **Batch Size:**  
  Change the `batch_size` variable in [`ocr_batch_resume.py`](ocr_batch_resume.py) to adjust how many files are processed per batch.

- **Input/Output Paths:**  
  Edit `INPUT_PATH` and `OUTPUT_PATH` at the top of [`ocr_batch_resume.py`](ocr_batch_resume.py) as needed.

## Project Structure

- [`ocr_batch_resume.py`](ocr_batch_resume.py): Main batch OCR script.
- `notebook.ipynb`: Jupyter notebook for prototyping and experimentation.

## License

GPL License

---

**Author:**  
Septian Jauhariansyah