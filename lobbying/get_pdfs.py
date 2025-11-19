"""
Download PDFs from lobbying filings CSV

This script reads the lobbying_filings.csv file and downloads all PDFs.
"""

import csv
import logging
from pathlib import Path

import requests
from pydantic import ValidationError

from models import LobbyingFiling

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class PDFDownloader:
    """Downloads PDFs from a CSV file of lobbying filings"""

    CSV_FILE = Path("lobbying_filings.csv")
    PDF_DIR = Path("pdfs")

    def __init__(self):
        self.session = requests.Session()
        self.pdf_dir = self.PDF_DIR
        self._ensure_pdf_directory()

    def _ensure_pdf_directory(self) -> None:
        """Create PDF directory if it doesn't exist"""
        self.pdf_dir.mkdir(exist_ok=True)
        logger.info(f"PDF directory: {self.pdf_dir}")

    def load_filings_from_csv(self) -> list[LobbyingFiling]:
        """
        Load filings from CSV file

        Returns:
            List of LobbyingFiling objects
        """
        if not self.CSV_FILE.exists():
            logger.error(f"CSV file not found: {self.CSV_FILE}")
            raise FileNotFoundError(f"CSV file not found: {self.CSV_FILE}")

        filings = []

        try:
            with open(self.CSV_FILE, 'r', encoding='utf-8') as f:
                # CSV from lobbying_filings.py has no header
                reader = csv.reader(f)
                for row in reader:
                    if len(row) >= 3:
                        try:
                            filing = LobbyingFiling(
                                name=row[0],
                                period=row[1],
                                url=row[2]
                            )
                            filings.append(filing)
                        except ValidationError as e:
                            logger.warning(f"Invalid row: {row} - {e}")
                    else:
                        logger.warning(f"Skipping row with insufficient columns: {row}")

            logger.info(f"Loaded {len(filings)} filings from CSV")
            return filings

        except Exception as e:
            logger.error(f"Error loading CSV: {e}")
            raise

    def download_pdf(self, filing: LobbyingFiling) -> bool:
        """
        Download a PDF file

        Args:
            filing: The filing to download

        Returns:
            True if downloaded, False if skipped (already exists) or failed
        """
        filepath = filing.get_filepath(self.pdf_dir)

        if filepath.exists():
            logger.debug(f"Skipped: {filepath.name} (already exists)")
            return False

        try:
            response = self.session.get(filing.url, timeout=60)
            response.raise_for_status()

            filepath.write_bytes(response.content)
            logger.info(f"Downloaded: {filepath.name}")
            return True

        except requests.RequestException as e:
            logger.error(f"Failed to download {filing.url}: {e}")
            logger.error(f"Status code: {getattr(e.response, 'status_code', 'N/A')}")
            return False

    def run(self) -> None:
        """Main execution method"""
        logger.info("Starting PDF downloader")

        # Load filings from CSV
        filings = self.load_filings_from_csv()

        # Download PDFs
        downloaded = 0
        for filing in filings:
            if self.download_pdf(filing):
                downloaded += 1

        logger.info(f"Download complete. {downloaded} new PDFs downloaded.")


def main():
    """Main entry point"""
    downloader = PDFDownloader()
    downloader.run()


if __name__ == "__main__":
    main()
