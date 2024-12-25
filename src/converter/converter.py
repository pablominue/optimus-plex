import ffmpeg
from src.crowler import Crowler
import typing as t
import os
from src.utils import PabLog

lg = PabLog(__name__)

class Converter:

    def __init__(self, output_format: str, delete_old: bool = True) -> None:
        self.output_format = output_format
        self.delete_old = delete_old

    @staticmethod
    def __convert(file:str, input_format:t.Union[str, list[str]], output_format:str) -> None:
        output = file.replace(f'.{input_format}', f'.{output_format}')
        ffmpeg.input(file).output(output).run()

    def run(self, input_format: str, base_path: str) -> None:
        crowler = Crowler(base_path=base_path)
        for path in crowler.crowl(input_format):
            try:
                self.__convert(path, input_format=input_format, output_format=self.output_format)
                lg.log.info("File %s Successfuly converted to %s", path, self.output_format)
                if self.delete_old:
                    os.remove(path)
                    lg.log.info("File %s has been deleted", path)
            except Exception as e:
                lg.log.error(e)
            