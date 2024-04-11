# PDF Tag Processor

## Overview
PDF Tag Processor is a Python tool designed to manage PDF files by extracting specific tags from each document, splitting the documents based on these tags, and organizing them into designated directories. This tool is especially useful for handling large volumes of PDF files in academic or corporate environments where document management can become cumbersome.

## Features
- **PDF Splitting:** Splits PDF files based on tags extracted from specified areas within the documents.
- **Tag Extraction:** Utilizes OCR technology to read and extract tags from each page of a PDF document.
- **Automatic Organization:** Files are automatically moved to pre-defined directories based on their extracted tags.
- **Logging:** Detailed logs are generated to track the processing status and handle errors efficiently.

## Installation

Before you begin, ensure you have Python installed on your machine. This project requires Python 3.6 or higher.

### Prerequisites
- Install `PyMuPDF` (also known as `fitz`), `PIL`, `pytesseract`, and `pdf2image`. You will also need to install Tesseract-OCR as the OCR engine.
  
  ```bash
  pip install PyMuPDF Pillow pytesseract pdf2image
  ```

  For Tesseract-OCR, please follow the installation instructions on their [official GitHub page](https://github.com/tesseract-ocr/tesseract).

### Clone the Repository
Clone this repository to your local machine to get started with the PDF Tag Processor.

```bash
git clone https://github.com/yourusername/prog_clearance_automate.git
cd prog_clearance_automate
```

## Usage
To use this tool, you need to specify the path to the directory containing your PDF files and the target root directory where the processed files should be organized.

### Running the Processor
Update the `directory_path` and `target_root` in the main script to reflect your specific directories.

```python
if __name__ == "__main__":
    directory_path = "path_to_your_pdf_directory"  # e.g., "/path/to/pdf/files"
    target_root = "path_to_your_target_directory"  # e.g., "/path/to/target/directory"
    pdf_processor = PDFProcessor(directory_path, target_root)
    tag_to_pdf_map = pdf_processor.process_all_pdfs()
    print(tag_to_pdf_map)
```

Run the script from your command line:

```bash
python pdf_processor.py
```

## Contributing
Contributions to the PDF Tag Processor are welcome! Here's how you can contribute:

- **Reporting Bugs:** Open an issue describing the bug and steps to reproduce it.
- **Suggesting Enhancements:** Open an issue with your suggestion.
- **Pull Requests:** Fork the repository, make your changes, and submit a pull request.

Please ensure your code adheres to the existing style to maintain the project's coherence.
