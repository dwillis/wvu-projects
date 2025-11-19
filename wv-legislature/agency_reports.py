"""
West Virginia Legislature Agency Reports Scraper

Scrapes agency reports from the WV Legislature website and saves them to CSV.
"""

import csv
import logging
from pathlib import Path
from typing import Optional

import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel, Field, HttpUrl

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class AgencyReport(BaseModel):
    """Schema for an agency report"""
    agency: str = Field(..., description="Agency name")
    title: str = Field(..., description="Report title")
    year: str = Field(..., description="Report year")
    url: str = Field(..., description="Report URL")

    def to_list(self) -> list:
        """Convert to list for CSV writing"""
        return [self.agency, self.title, self.year, self.url]


class AgencyReportsScraper:
    """Scraper for WV Legislature agency reports"""

    BASE_URL = "http://www.wvlegislature.gov"
    REPORTS_URL = f"{BASE_URL}/Reports/Agency_Reports/agencylist_all.cfm"
    ALL_REPORTS_CSV = Path("all_reports.csv")
    NEW_REPORTS_CSV = Path("new_reports.csv")

    def __init__(self, start_year: int = 2001, end_year: int = 2025):
        """
        Initialize the scraper

        Args:
            start_year: First year to scrape (inclusive)
            end_year: Last year to scrape (exclusive)
        """
        self.session = requests.Session()
        self.start_year = start_year
        self.end_year = end_year
        self.previous_urls: set[str] = set()

    def load_existing_reports(self) -> None:
        """Load existing report URLs from CSV"""
        if not self.ALL_REPORTS_CSV.exists():
            logger.info("No existing CSV file found, creating new one")
            self.ALL_REPORTS_CSV.write_text("agency,title,year,url\n")
            return

        try:
            with open(self.ALL_REPORTS_CSV, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                self.previous_urls = {
                    row['url'] for row in reader
                    if row['url'] and row['url'] != 'No Report'
                }
            logger.info(f"Loaded {len(self.previous_urls)} existing report URLs")
        except Exception as e:
            logger.error(f"Error loading existing reports: {e}")
            raise

    def fetch_reports_for_year(self, year: int) -> list[AgencyReport]:
        """
        Fetch reports for a specific year

        Args:
            year: The year to fetch reports for

        Returns:
            List of AgencyReport objects
        """
        logger.info(f"Fetching reports for year {year}")
        reports = []

        try:
            response = self.session.post(
                self.REPORTS_URL,
                data={'report_year': year},
                timeout=30
            )
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            rows = soup.find_all('tr')[1:-1]  # Skip header and footer rows

            for row in rows:
                try:
                    cells = row.find_all('td')
                    if len(cells) < 3:
                        continue

                    agency = cells[0].text.strip()
                    title = cells[1].text.strip()
                    year_str = cells[2].text.strip()

                    # Check if there's a link
                    link = row.find('a')
                    if link and 'href' in link.attrs:
                        url = self.BASE_URL + link['href']
                        reports.append(
                            AgencyReport(
                                agency=agency,
                                title=title,
                                year=year_str,
                                url=url
                            )
                        )
                except Exception as e:
                    logger.warning(f"Error parsing row in year {year}: {e}")
                    continue

            logger.info(f"Found {len(reports)} reports for year {year}")
            return reports

        except requests.RequestException as e:
            logger.error(f"Error fetching reports for year {year}: {e}")
            return []

    def scrape_all_reports(self) -> list[AgencyReport]:
        """Scrape reports for all configured years"""
        logger.info(f"Scraping reports from {self.start_year} to {self.end_year-1}")
        all_reports = []

        for year in range(self.start_year, self.end_year):
            reports = self.fetch_reports_for_year(year)
            all_reports.extend(reports)

        logger.info(f"Total reports scraped: {len(all_reports)}")
        return all_reports

    def filter_new_reports(self, reports: list[AgencyReport]) -> list[AgencyReport]:
        """
        Filter out reports that already exist

        Args:
            reports: List of all reports

        Returns:
            List of only new reports
        """
        # Get all unique URLs from scraped reports
        all_urls = {r.url for r in reports}

        # Find new URLs
        new_urls = all_urls - self.previous_urls

        # Filter reports to only include new ones
        new_reports = [r for r in reports if r.url in new_urls]

        logger.info(f"Found {len(new_reports)} new reports")
        return new_reports

    def save_reports(
        self,
        reports: list[AgencyReport],
        filepath: Path,
        append: bool = False
    ) -> None:
        """
        Save reports to CSV

        Args:
            reports: List of reports to save
            filepath: Path to save to
            append: Whether to append or overwrite
        """
        if not reports:
            logger.info(f"No reports to save to {filepath}")
            return

        mode = 'a' if append else 'w'

        try:
            with open(filepath, mode, encoding='utf-8', newline='') as f:
                writer = csv.writer(f)

                # Write header if creating new file
                if not append or not filepath.exists():
                    writer.writerow(['agency', 'title', 'year', 'url'])

                for report in reports:
                    writer.writerow(report.to_list())

            logger.info(f"Successfully saved {len(reports)} reports to {filepath}")
        except Exception as e:
            logger.error(f"Error saving reports to {filepath}: {e}")
            raise

    def run(self) -> None:
        """Main execution method"""
        logger.info("Starting agency reports scraper")

        # Load existing reports
        self.load_existing_reports()

        # Scrape all reports
        all_reports = self.scrape_all_reports()

        # Filter for new reports
        new_reports = self.filter_new_reports(all_reports)

        # Save new reports to separate file
        self.save_reports(new_reports, self.NEW_REPORTS_CSV, append=False)

        # Append new reports to all reports file
        if new_reports:
            self.save_reports(new_reports, self.ALL_REPORTS_CSV, append=True)

        logger.info(f"Scraper completed. {len(new_reports)} new reports added.")


def main():
    """Main entry point"""
    scraper = AgencyReportsScraper(start_year=2001, end_year=2025)
    scraper.run()


if __name__ == "__main__":
    main()
