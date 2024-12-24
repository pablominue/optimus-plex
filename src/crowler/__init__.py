import os
import typing as t

class Crowler:
    def __init__(self, base_path: str):
        self.path = base_path
        
    def crowl(self, search_format: str) -> t.Generator[t.Any, t.Any, t.Any]:
        if not os.path.exists(self.path):
            raise FileNotFoundError(f"Base Path: {self.path} can not be found")
        for dirpath, _, files in os.walk(self.path):
            for file in files:
                if file.endswith(search_format):
                    yield os.path.join(dirpath,file)
