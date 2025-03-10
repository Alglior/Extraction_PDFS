#split pdf page into png .... ATTENTION THIS MAKE FILES BIGGER
import fitz
import os
from pathlib import Path
import logging
from concurrent.futures import ProcessPoolExecutor
import multiprocessing

class FastPDFExtractor:
    def __init__(self, pdf_path: str, output_dir: str, dpi: int = 300):
        """
        Initialize the extractor with PDF path and output directory
        """
        self.pdf_path = pdf_path
        self.pdf_name = Path(pdf_path).stem
        self.output_dir = os.path.join(output_dir, self.pdf_name)
        self.dpi = dpi
        
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    @staticmethod
    def process_page(args):
        """
        Static method to process a single page (needed for multiprocessing)
        """
        pdf_path, page_num, output_path, dpi = args
        try:
            # Open the PDF file within the process
            doc = fitz.open(pdf_path)
            page = doc[page_num]
            
            # Convert page to high-resolution image
            matrix = fitz.Matrix(dpi/72, dpi/72)
            pix = page.get_pixmap(matrix=matrix)
            pix.save(output_path)
            
            # Close the document
            doc.close()
            return True
        except Exception as e:
            print(f"Error processing page {page_num + 1}: {e}")
            return False

    def extract_pages(self):
        """
        Extract all pages from PDF as PNG files using multiple processes
        """
        try:
            # Create output directory
            os.makedirs(self.output_dir, exist_ok=True)
            
            # Open PDF to get page count
            doc = fitz.open(self.pdf_path)
            total_pages = len(doc)
            doc.close()  # Close immediately as we'll reopen in each process
            
            # Prepare arguments for multiprocessing
            process_args = []
            for page_num in range(total_pages):
                output_path = os.path.join(self.output_dir, f"page_{page_num + 1}.png")
                # Pass the PDF path instead of page object
                process_args.append((self.pdf_path, page_num, output_path, self.dpi))
            
            # Use ProcessPoolExecutor for parallel processing
            cpu_count = multiprocessing.cpu_count()
            max_workers = max(1, cpu_count - 1)  # Leave one CPU core free
            
            self.logger.info(f"Starting extraction of {total_pages} pages using {max_workers} processes")
            
            with ProcessPoolExecutor(max_workers=max_workers) as executor:
                results = list(executor.map(self.process_page, process_args))
            
            successful_pages = sum(results)
            self.logger.info(f"Extraction completed: {successful_pages}/{total_pages} pages processed")
            
        except Exception as e:
            self.logger.error(f"Error during extraction: {e}")
            raise

def batch_process_pdfs(input_dir: str = "pdfs", output_dir: str = "extracted_pages", dpi: int = 300):
    """
    Process all PDFs in the input directory
    """
    try:
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Get all PDF files
        pdf_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.pdf')]
        
        if not pdf_files:
            print("No PDF files found in the input directory")
            return
        
        print(f"Found {len(pdf_files)} PDF files to process")
        
        # Process each PDF
        for pdf_file in pdf_files:
            pdf_path = os.path.join(input_dir, pdf_file)
            print(f"Processing: {pdf_file}")
            
            extractor = FastPDFExtractor(pdf_path, output_dir, dpi)
            extractor.extract_pages()
            
        print("All PDFs processed successfully")
        
    except Exception as e:
        print(f"Error in batch processing: {e}")

if __name__ == "__main__":
    batch_process_pdfs()