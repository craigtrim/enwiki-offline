# -*- coding: utf-8 -*-
""" Parse the EnWiki all-titles File """


from collections import Counter
from typing import Dict, Iterator

from baseblock import FileIO

from enwiki_offline.parser.dto import calculate_md5


class ParseEnwikiAllTitles(object):
    """ Parse the EnWiki all-titles File """

    def __init__(self):
        """ Change Log

        Created:
            9-Apr-2024
            craigtrim@gmail.com
        """
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

    @staticmethod
    def _write_file(ch2: str, c: Counter) -> None:
        pass

    def process(self, input_path: str) -> None:

        c: Counter = Counter()
        prior_ch2 = None

        i = 0

        for line in self._read_file(input_path):
            if not line or not len(line):
                break

            tokens = line.split('\t')
            if not tokens or not len(tokens) == 2:
                continue

            title: str = tokens[1].strip()
            if title == 'page_title':
                continue

            if len(title) < 3:
                continue

            if not title[:2].isalpha():
                continue

            if '_' in title:
                title = title.replace('_', ' ')

            ch2 = title[:2].lower()

            if not prior_ch2:
                prior_ch2 = ch2
                print(f"initialize prior-ch2={ch2}")

            if ch2 != prior_ch2:
                print(f"ch2={prior_ch2} = {len(c)}")
                prior_ch2 = ch2
                print(f"reset prior-ch2={prior_ch2}")
                c = Counter()

            c.update({title, 1})

            i += 1
            if i > 50000:
                break
