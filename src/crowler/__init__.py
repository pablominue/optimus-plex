import os
import typing as t
from src.utils import PabLog

lg = PabLog(__name__)

class Crowler:
    def __init__(self, base_path: str):
        self.path = base_path
        
    def crowl(self, search_format: t.Union[str, list[str]]) -> t.Generator[t.Any, t.Any, t.Any]:
        """
        Crawl through the specified base path and yield file paths that match the given search format.

        This method walks through the directory structure starting from the base path,
        and yields the full path of each file that matches the specified search format.

        Args:
            search_format (Union[str, list[str]]): A string or list of strings representing
                the file extensions to search for. If a list is provided, it will be
                converted to a tuple.

        Yields:
            str: The full path of each file that matches the search format.

        Raises:
            FileNotFoundError: If the specified base path does not exist.

        """
        if not os.path.exists(self.path):
            raise FileNotFoundError(f"Base Path: {self.path} can not be found")
        for dirpath, _, files in os.walk(self.path):
            for file in files:
                if isinstance(search_format, list):
                    search_format = tuple(search_format)
                if file.endswith(search_format):
                    lg.log.info("Target File ready for Conversion: %s", file)
                    yield os.path.join(dirpath,file)