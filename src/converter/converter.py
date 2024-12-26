import ffmpeg
from src.crowler import Crowler
import typing as t
import os
from src.utils import PabLog

lg = PabLog(__name__)

class Converter:
    """
    A class for converting files from one format to another.
    """

    def __init__(self, output_format: str, delete_old: bool = True) -> None:
        """
        Initialize the Converter object.

        Args:
            output_format (str): The desired output format for the converted files.
            delete_old (bool, optional): Whether to delete the original files after conversion. Defaults to True.
        """
        self.output_format = output_format
        self.delete_old = delete_old

    @staticmethod
    def __convert(file: str, input_format: t.Union[str, list[str]], output_format: str) -> None:
        """
        Convert a single file to the specified output format.

        Args:
            file (str): The path to the file to be converted.
            input_format (Union[str, list[str]]): The current format(s) of the input file.
            output_format (str): The desired output format.

        Returns:
            None
        """
        output = file.replace(f'.{input_format}', f'.{output_format}')
        ffmpeg.input(file).output(output).run()

    def run(self, input_format: str, base_path: str) -> t.Generator[t.Any, t.Any, t.Any]:
        """
        Run the conversion process on all files with the specified input format in the given base path.

        Args:
            input_format (str): The format of the files to be converted.
            base_path (str): The base directory path where the files are located.

        Returns:
            None
        """
        crowler = Crowler(base_path=base_path)
        for path in crowler.crowl(input_format):
            try:
                self.__convert(path, input_format=input_format, output_format=self.output_format)
                lg.log.info("File %s Successfuly converted to %s", path, self.output_format)
                if self.delete_old:
                    os.remove(path)
                    lg.log.info("File %s has been deleted", path)
                    yield True
            except Exception as e:
                lg.log.error(e)
                yield False