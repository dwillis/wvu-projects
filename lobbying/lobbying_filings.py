"""
West Virginia Lobbying Filings Scraper

Scrapes lobbying filings from the WV Ethics Commission website.
"""

import csv
import logging
import sys
from pathlib import Path
from typing import Optional

import requests
from bs4 import BeautifulSoup

from models import LobbyingFiling

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class LobbyingFilingsScraper:
    """Scraper for WV lobbying filings"""

    BASE_URL = "https://ethics.wv.gov"
    CSV_FILE = Path("lobbying_filings.csv")
    PDF_DIR = Path("pdfs")

    def __init__(self, registration_cycle: str):
        """
        Initialize the scraper

        Args:
            registration_cycle: The registration cycle (e.g., "2019-2020", "2021-2022")
        """
        self.session = requests.Session()
        self.registration_cycle = registration_cycle
        self.pdf_dir = self.PDF_DIR
        self._ensure_pdf_directory()

    def _ensure_pdf_directory(self) -> None:
        """Create PDF directory if it doesn't exist"""
        self.pdf_dir.mkdir(exist_ok=True)
        logger.info(f"PDF directory: {self.pdf_dir}")

    def _get_cycle_url(self) -> str:
        """
        Get the URL for the registration cycle page

        Returns:
            Full URL for the cycle
        """
        if self.registration_cycle == '2019-2020':
            return f"{self.BASE_URL}/lobbyist/Pages/{self.registration_cycle}.aspx"
        else:
            return f"{self.BASE_URL}/lobbyist/Pages/{self.registration_cycle}-Registration-Cycle.aspx"

    def fetch_filings(self) -> list[LobbyingFiling]:
        """
        Fetch all lobbying filings for the registration cycle

        Returns:
            List of LobbyingFiling objects
        """
        url = self._get_cycle_url()
        logger.info(f"Fetching filings from: {url}")

        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()

            # Remove newlines for easier parsing
            html = "".join(line.strip() for line in response.text.split('\n'))
            soup = BeautifulSoup(html, 'html.parser')

            # Find all links to PDF documents
            links = [
                x['href'] for x in soup.find_all('a')
                if 'href' in x.attrs and 'SiteCollectionDocuments' in x['href']
            ]

            logger.info(f"Found {len(links)} filing links")

            filings = []
            for link in links:
                filing = self._parse_filing_link(link)
                if filing:
                    filings.append(filing)

            logger.info(f"Successfully parsed {len(filings)} filings")
            return filings

        except requests.RequestException as e:
            logger.error(f"Error fetching filings: {e}")
            raise

    def _parse_filing_link(self, link: str) -> Optional[LobbyingFiling]:
        """
        Parse a filing link to extract information

        Args:
            link: The href value from the link

        Returns:
            LobbyingFiling object or None if parsing fails
        """
        try:
            url = self.BASE_URL + link
            parts = link.split('/')

            if len(parts) < 6:
                logger.warning(f"Unexpected link format: {link}")
                return None

            period = parts[4]
            # Extract name from filename, removing period and normalizing
            name = (
                parts[5].split('.')[0]
                .replace(period, '')
                .replace('%20', ' ')
                .strip()
                .upper()
            )

            return LobbyingFiling(name=name, period=period, url=url)

        except Exception as e:
            logger.warning(f"Error parsing link {link}: {e}")
            return None

    def save_filings_to_csv(self, filings: list[LobbyingFiling]) -> None:
        """
        Save filings to CSV file

        Args:
            filings: List of filings to save
        """
        if not filings:
            logger.warning("No filings to save")
            return

        try:
            with open(self.CSV_FILE, 'w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f)
                for filing in filings:
                    writer.writerow(filing.to_list())

            logger.info(f"Saved {len(filings)} filings to {self.CSV_FILE}")
        except Exception as e:
            logger.error(f"Error saving filings to CSV: {e}")
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
            return False

    def download_all_pdfs(self, filings: list[LobbyingFiling]) -> int:
        """
        Download all PDF files

        Args:
            filings: List of filings to download

        Returns:
            Number of files downloaded (excluding skipped files)
        """
        logger.info(f"Downloading {len(filings)} PDFs...")
        downloaded = 0

        for filing in filings:
            if self.download_pdf(filing):
                downloaded += 1

        logger.info(f"Downloaded {downloaded} new PDFs")
        return downloaded

    def run(self) -> None:
        """Main execution method"""
        logger.info(f"Starting lobbying filings scraper for cycle: {self.registration_cycle}")

        # Fetch filings
        filings = self.fetch_filings()

        # Save to CSV
        self.save_filings_to_csv(filings)

        # Download PDFs
        self.download_all_pdfs(filings)

        logger.info("Scraper completed successfully")


def main():
    """Main entry point"""
    if len(sys.argv) != 2:
        print("Usage: python lobbying_filings.py <registration_cycle>")
        print("Example: python lobbying_filings.py 2021-2022")
        sys.exit(1)

    registration_cycle = sys.argv[1]
    scraper = LobbyingFilingsScraper(registration_cycle)
    scraper.run()


if __name__ == "__main__":
    main()
