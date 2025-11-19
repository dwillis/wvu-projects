"""
West Virginia Meeting Notices Scraper

Scrapes meeting notices from the WV Secretary of State website and saves them to CSV.
"""

import csv
import logging
from pathlib import Path
from typing import Optional

import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel, Field, field_validator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class MeetingNotice(BaseModel):
    """Schema for a meeting notice"""
    id: str = Field(..., description="Unique identifier for the meeting notice")
    date: str = Field(..., description="Meeting date")
    time: str = Field(..., description="Meeting time")
    agency: str = Field(..., description="Agency name")
    subagency: Optional[str] = Field(None, description="Subagency name if applicable")
    location: str = Field(..., description="Meeting location")
    purpose: str = Field(..., description="Purpose of the meeting")
    notes: str = Field(..., description="Additional notes")

    @field_validator('location')
    @classmethod
    def clean_location(cls, v: str) -> str:
        """Clean up location text"""
        return v.replace('\r\n', ' ').replace('  ', ' ').strip()

    def to_list(self) -> list:
        """Convert to list for CSV writing"""
        return [
            self.id,
            self.date,
            self.time,
            self.agency,
            self.subagency,
            self.location,
            self.purpose,
            self.notes
        ]


class MeetingNoticesScraper:
    """Scraper for WV meeting notices"""

    BASE_URL = "http://apps.sos.wv.gov/adlaw/meetingnotices/"
    CSV_FILE = Path("meeting_notices.csv")

    def __init__(self):
        self.session = requests.Session()
        self.previous_ids: set[str] = set()

    def load_existing_notices(self) -> None:
        """Load existing notice IDs from CSV"""
        if not self.CSV_FILE.exists():
            logger.info("No existing CSV file found, creating new one")
            self.CSV_FILE.write_text("id,date,time,agency,subagency,location,purpose,notes\n")
            return

        try:
            with open(self.CSV_FILE, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                self.previous_ids = {row['id'] for row in reader}
            logger.info(f"Loaded {len(self.previous_ids)} existing notice IDs")
        except Exception as e:
            logger.error(f"Error loading existing notices: {e}")
            raise

    def fetch_page(self, url: str) -> BeautifulSoup:
        """Fetch and parse a page"""
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return BeautifulSoup(response.text, 'html.parser')
        except requests.RequestException as e:
            logger.error(f"Error fetching {url}: {e}")
            raise

    def parse_meeting_notice(self, link) -> Optional[MeetingNotice]:
        """Parse a single meeting notice from a link"""
        try:
            url = self.BASE_URL + link['href']
            notice_id = url.split('=')[1]

            # Parse date and time from link text
            date, time = link.text.split(' -- ')

            # Fetch the detail page
            soup = self.fetch_page(url)

            # Parse agency information
            th = soup.find('th')
            if th and th.find('h2'):
                h2 = th.find('h2')
                agency = h2.find('br').previous if h2.find('br') else h2.text
                em_tags = h2.find_all('em')
                subagency = " ".join([x.text for x in em_tags]) if em_tags else None
            else:
                agency = th.text if th else "Unknown"
                subagency = None

            # Parse details
            details = soup.find_all('td')
            if len(details) < 4:
                logger.warning(f"Insufficient details for notice {notice_id}")
                return None

            location_pre = details[1].find('pre')
            location = location_pre.text if location_pre else details[1].text

            purpose_text = details[2].text
            purpose = purpose_text.split('Purpose: ')[1] if 'Purpose: ' in purpose_text else purpose_text

            notes_text = details[3].text
            notes = notes_text.split('Notes: ')[1] if 'Notes: ' in notes_text else notes_text

            return MeetingNotice(
                id=notice_id,
                date=date,
                time=time,
                agency=agency,
                subagency=subagency,
                location=location,
                purpose=purpose,
                notes=notes
            )
        except Exception as e:
            logger.error(f"Error parsing meeting notice from {link.get('href', 'unknown')}: {e}")
            return None

    def scrape_notices(self) -> list[MeetingNotice]:
        """Scrape all meeting notices from the main page"""
        logger.info("Fetching meeting notices...")

        soup = self.fetch_page(self.BASE_URL)
        table = soup.find("table", {"id": "tableResults"})

        if not table:
            logger.error("Could not find results table")
            return []

        links = table.find_all('a')
        logger.info(f"Found {len(links)} meeting notice links")

        notices = []
        for link in links:
            notice = self.parse_meeting_notice(link)
            if notice:
                notices.append(notice)

        logger.info(f"Successfully parsed {len(notices)} notices")
        return notices

    def save_new_notices(self, notices: list[MeetingNotice]) -> int:
        """Save new notices to CSV and return count of new notices"""
        new_notices = [n for n in notices if n.id not in self.previous_ids]

        if not new_notices:
            logger.info("No new notices to save")
            return 0

        logger.info(f"Saving {len(new_notices)} new notices")

        try:
            with open(self.CSV_FILE, 'a', encoding='utf-8', newline='') as f:
                writer = csv.writer(f)
                for notice in new_notices:
                    writer.writerow(notice.to_list())

            logger.info(f"Successfully saved {len(new_notices)} new notices")
            return len(new_notices)
        except Exception as e:
            logger.error(f"Error saving notices: {e}")
            raise

    def run(self) -> None:
        """Main execution method"""
        logger.info("Starting meeting notices scraper")

        self.load_existing_notices()
        notices = self.scrape_notices()
        new_count = self.save_new_notices(notices)

        logger.info(f"Scraper completed. {new_count} new notices added.")


def main():
    """Main entry point"""
    scraper = MeetingNoticesScraper()
    scraper.run()


if __name__ == "__main__":
    main()
