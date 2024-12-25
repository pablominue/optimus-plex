import os
import typing as t
from src.utils import PabLog

lg = PabLog(__name__)

class Crowler:
    def __init__(self, base_path: str):
        self.path = base_path
        
    def crowl(self, search_format: t.Union[str, list[str]]) -> t.Generator[t.Any, t.Any, t.Any]:
        if not os.path.exists(self.path):
            raise FileNotFoundError(f"Base Path: {self.path} can not be found")
        for dirpath, _, files in os.walk(self.path):
            for file in files:
                if isinstance(search_format, list):
                    search_format = tuple(search_format)
                if file.endswith(search_format):
                    lg.log.info("Target File ready for Conversion: %s", file)
                    yield os.path.join(dirpath,file)
