# open_pdf_file.py

from ast import List
from pathlib import Path
import pandas as pd
import tabula


class OpenPDF:
    """Class for extract tables from PDF file into DataFrame"""

    def __init__(self, path: str) -> None:
        """Initialize OpenPDF"""
        # Check if file exist and has .pdf extensions
        self.empty_data_frame = Path(path).is_file() and path.lower().endswith(
            ".pdf"
        )
        if not self.empty_data_frame:
            return
        # Extract all tables from PDF into DataFrame
        self.data_frames: List[pd.DataFrame] = tabula.read_pdf(
            path, pages="all"
        )

    def get_pdf_tables(self):
        """Returns pandas data frames"""
        return self.data_frames
