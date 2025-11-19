"""
Pydantic models for lobbying data
"""

from pathlib import Path
from pydantic import BaseModel, Field


class LobbyingFiling(BaseModel):
    """Schema for a lobbying filing"""
    name: str = Field(..., description="Lobbyist name")
    period: str = Field(..., description="Filing period")
    url: str = Field(..., description="PDF URL")

    def to_list(self) -> list:
        """Convert to list for CSV writing"""
        return [self.name, self.period, self.url]

    def get_filename(self) -> str:
        """Get the PDF filename from the URL"""
        return self.url.split('/')[-1]

    def get_filepath(self, directory: Path) -> Path:
        """Get the full file path for saving the PDF"""
        return directory / self.get_filename()
