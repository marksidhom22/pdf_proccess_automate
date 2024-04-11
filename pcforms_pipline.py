from PIL import Image
import pytesseract
from pdf2image import convert_from_path
import fitz  # PyMuPDF
import os
import re
import logging
from datetime import datetime

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\marks\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
import shutil

class PDFProcessor:
    def __init__(self, directory_path, target_root):
        self.directory_path = directory_path
        self.target_root = target_root
        self.output_dir = self.create_output_directory()
        self.setup_logging()

    def create_output_directory(self):
        date_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        output_dir = os.path.join(os.getcwd(), date_str)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        return output_dir

    def setup_logging(self):
        log_filename = os.path.join(self.output_dir, "process.log")
        logging.basicConfig(filename=log_filename, level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')

    @staticmethod
    def sanitize_filename(filename):
        illegal_chars = r'[\<\>\:\"\/\\\|\?\*]'
        return re.sub(illegal_chars, '_', filename)

    def process_all_pdfs(self):
        pdf_files = [f for f in os.listdir(self.directory_path) if f.endswith('.pdf')]
        tag_to_pdf_map = {}
        for pdf_file in pdf_files:
            pdf_path = os.path.join(self.directory_path, pdf_file)
            tag_to_pdf = self.split_pdf_by_tag(pdf_path)
            for tag, pdf_filename in tag_to_pdf.items():
                target_dir = self.find_target_directory(tag)
                if target_dir:
                    self.copy_file_to_directory(pdf_filename, target_dir)
            tag_to_pdf_map[pdf_file] = tag_to_pdf
        return tag_to_pdf_map

    def split_pdf_by_tag(self, pdf_path):
        tag_to_pdf = {}
        doc = fitz.open(pdf_path)
        try:
            for page in doc:
                tag = self.extract_tag(page)
                if tag:
                    pdf_filename = self.save_page_as_pdf(page, pdf_path)
                    tag_to_pdf[tag[0]] = pdf_filename
        except Exception as e:
            logging.error(f"Failed to process PDF {pdf_path}: {e}")
        finally:
            doc.close()
        return tag_to_pdf

    def find_target_directory(self, tag):
        for root, dirs, files in os.walk(self.target_root):
            for name in dirs:
                if tag in name:
                    return os.path.join(root, name)
        return None

    def copy_file_to_directory(self, source, destination):
        try:
            shutil.copy(source, destination)
            logging.info(f"File {source} copied to {destination}")
        except Exception as e:
            logging.error(f"Failed to copy {source} to {destination}: {e}")

    def extract_tag(self, page):
        clip_rect = fitz.Rect(473, 134, 528, 146)
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2), clip=clip_rect)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        text = pytesseract.image_to_string(img)
        return re.search(r'^\d+$', text)

    def save_page_as_pdf(self, page, pdf_path):
        base_name = os.path.splitext(os.path.basename(pdf_path))[0]
        pdf_filename = f"{base_name}-page-{page.number}.pdf"
        pdf_full_path = os.path.join(self.output_dir, pdf_filename)
        
        mat = fitz.Matrix(2, 2)
        pix = page.get_pixmap(matrix=mat)
        img = Image.frombytes("RGB", [1224, 1584], pix.samples)

        img.save(pdf_full_path, "PDF", resolution=200.0)
        return pdf_full_path

if __name__ == "__main__":
    directory_path = "."  # Replace with the path to your directory
    target_root = "P:\\LeMark (Graduation)\\Grad Files\\202360 grad files"  # Replace with your target root directory
    pdf_processor = PDFProcessor(directory_path, target_root)
    tag_to_pdf_map = pdf_processor.process_all_pdfs()
    print(tag_to_pdf_map)
