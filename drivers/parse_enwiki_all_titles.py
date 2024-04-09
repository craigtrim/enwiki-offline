# -*- coding: utf-8 -*-
""" Parse the EnWiki all-titles File """


from collections import defaultdict
from json import dump
from typing import Iterator

from baseblock import BaseObject, FileIO, Stopwatch


class ParseEnwikiAllTitles(BaseObject):
    """
    Parse the EnWiki all-titles File

    This script reads a large file containing titles from the English Wikipedia (EnWiki) and processes it to generate a dictionary of titles. The dictionary is then written to separate JSON files based on the first three characters of each title.

    The input file should be a tab-separated values (TSV) file with two columns: page_id and page_title. The script ignores any lines that do not conform to this format.

    The processed dictionary is structured as follows:
    {
        "title1": ["original_title1", "original_title2", ...],
        "title2": ["original_title3", "original_title4", ...],
        ...
    }

    Usage:
        python parse_enwiki_all_titles.py <input_file_path>

    Arguments:
        input_file_path (str): The path to the input file.

    Example:
        python parse_enwiki_all_titles.py /path/to/input_file.tsv
    """

    def __init__(self):
        """ Change Log

        Created:
            9-Apr-2024
            craigtrim@gmail.com
        """
        BaseObject.__init__(self, __name__)
        self._output_path = FileIO.join_cwd('resources/enwiki')
        FileIO.exists_or_error(self._output_path)

    @staticmethod
    def _read_file(file_path: str) -> Iterator[str]:
        """
        Reads a large file line by line and yields each line.

        Args:
            file_path (str): The path to the file to be read.

        Yields:
            str: Each line of the file.

        """
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                yield line

    def _write_file(self, ch3: str, d: dict) -> None:
        """
        Writes the given dictionary `d` to a JSON file with the name `ch2` in the appropriate directory.

        Args:
            ch2 (str): The name of the file to be written.
            d (dict): The dictionary to be written to the file.

        Returns:
            None
        """
        ch_path = FileIO.join(self._output_path, ch3[0], ch3[:2])
        FileIO.exists_or_create(ch_path)
        file_path = FileIO.join(ch_path, f"{ch3}.json")

        with open(file_path, 'w') as file:
            dump(d, file, separators=(',', ':'))

    def process(self, input_path: str) -> None:
        """
        Process the input file and generate a dictionary of titles.

        Args:
            input_path (str): The path to the input file.

        Returns:
            None
        """

        d = defaultdict(list)
        prior_ch3 = None

        i = 0
        sw = Stopwatch()

        for line in self._read_file(input_path):
            if not line or not len(line):
                break

            tokens = line.split('\t')
            if not tokens or not len(tokens) == 2:
                continue

            title: str = tokens[1].strip()
            if title == 'page_title':
                continue

            if len(title) < 4:
                continue

            if '_' in title:
                title = title.replace('_', ' ')

            original_title = title
            title = title.lower()
            ch3 = title[:3]

            if not all(c.isalpha() and 'a' <= c <= 'z' for c in ch3):
                continue

            if '(' in title:
                title = title.split('(')[0].strip()

            if ':' in title:
                title = title.split(':')[0].strip()

            if ' - ' in title:
                title = title.split(' - ')[0].strip()

            if len(title) < 4:
                continue

            if not prior_ch3:
                prior_ch3 = ch3

            if ch3 != prior_ch3:
                self._write_file(ch2=prior_ch3, d=dict(d))
                self.logger.debug(
                    f"Finished: {prior_ch3} with {len(d)} elapsed {str(sw)}")
                prior_ch3 = ch3
                d = defaultdict(list)

            # c.update({title, 1})
            if not any(s.lower() == original_title.lower() for s in d[title]):
                d[title].append(original_title)

            i += 1


def main(input_path):
    ParseEnwikiAllTitles().process(input_path=input_path)


if __name__ == "__main__":
    import plac

    plac.call(main)
