import ffmpeg
from src.crowler import Crowler
import typing as t
from src.utils import PabLog

lg = PabLog(__name__)

class Converter:

    def __init__(self, output_format: str) -> None:
        self.output_format = output_format

    @staticmethod
    def __convert(file:str, input_format:t.Union[str, list[str]], output_format:str) -> None:
        output = file.replace(f'.{input_format}', f'.{output_format}')
        ffmpeg.input(file).output(output).run()

    def run(self, input_format: str, base_path: str) -> None:
        crowler = Crowler(base_path=base_path)
        for path in crowler.crowl(input_format):
            try:
                self.__convert(path, input_format=input_format, output_format=self.output_format)
                lg.log.info("File %s Successfuly converted", path)
            except Exception as e:
                lg.log.error(e)
            