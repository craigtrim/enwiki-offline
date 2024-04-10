# -*- coding: utf-8 -*-
""" Parse the EnWiki all-titles File """


from collections import defaultdict
from copy import deepcopy
from json import dump
from typing import Iterator, List

from baseblock import BaseObject, Stopwatch

from enwiki_offline.utils import (calculate_md5, exists, exists_or_create,
                                  exists_or_error, join, join_cwd,
                                  write_string)


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
        self._output_path = join_cwd('resources/enwiki')
        exists_or_error(self._output_path)

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

    def _write_file(self, prefix_1: str, type: str, values: List[str]) -> None:
        """
        Writes the given dictionary `d` to a JSON file with the name `ch2` in the appropriate directory.

        Args:
            ch2 (str): The name of the file to be written.
            d (dict): The dictionary to be written to the file.

        Returns:
            None
        """
        ch_path = join(self._output_path, type)
        exists_or_create(ch_path)
        file_path = join(ch_path, f"{prefix_1}.txt")
        write_string(input_text=' '.join(values), file_path=file_path)

    @staticmethod
    def _normalize_title(title: str) -> str | None:
        title = title.lower().strip()

        whitelist = [' ', '.', ',', ':']
        if not all(c in whitelist or c.isalpha() and 'a' <= c <= 'z' for c in title):
            return None

        if '(' in title:
            title = title.split('(')[0].strip()

        if ':' in title:
            title = title.split(':')[0].strip()

        if ' - ' in title:
            title = title.split(' - ')[0].strip()

        if len(title) < 4:
            return None

        return title

    @staticmethod
    def _get_title(line: str) -> str | None:
        if not line or not len(line):
            return None

        tokens = line.split('\t')
        if not tokens or not len(tokens) == 2:
            return None

        title: str = tokens[1].strip()
        if title == 'page_title':
            return None

        if len(title) < 4:
            return None

        return title

    def process(self, input_path: str) -> None:
        """
        Process the input file and generate a dictionary of titles.

        Args:
            input_path (str): The path to the input file.

        Returns:
            None
        """

        # for status logging
        i = 0
        sw = Stopwatch()

        # can't guarantee the sort order of the iput file
        # so it has to be loaded into a dictionary first
        # approx 23,250,000 lines in 2-3 minutes
        d_entities = defaultdict(list)

        for line in self._read_file(input_path):

            title = self._get_title(line)
            if not title or not len(title):
                continue

            if '_' in title:
                title = title.replace('_', ' ')

            original_title = deepcopy(title)

            title = self._normalize_title(title)
            if not title or not len(title):
                continue

            d_entities[title].append(original_title)

            if i == 0:
                self.logger.info(f"Starting ~26 million lines in 2-3 minutes")
            elif i % 1000000 == 0:
                self.logger.info(f"Line {i} in {str(sw)}")

            i += 1

        self.logger.info(
            f"Finished Loading Dictionary in {str(sw)} with {len(d_entities)} elements")

        ambiguous_entities: List[str] = []
        unambiguous_entities: List[str] = []

        def bucket(entity: str) -> None:
            if len(d_entities[entity]) > 1:
                ambiguous_entities.append(entity)
            else:
                unambiguous_entities.append(entity)

        [
            bucket(entity) for entity in d_entities
        ]

        d_md5 = defaultdict(set)

        def to_md5(entities: List[str], type: str) -> None:

            for entity in entities:
                md5 = calculate_md5(entity)
                if md5[:2] not in d_md5:
                    d_md5[md5[:2]] = []
                d_md5[md5[:2]].append(md5[2:])

            for prefix_1 in d_md5:
                self._write_file(prefix_1=prefix_1, type=type,
                                 values=d_md5[prefix_1])

        to_md5(entities=ambiguous_entities, type="ambiguous")
        to_md5(entities=unambiguous_entities, type="unambiguous")


def main(input_path):
    ParseEnwikiAllTitles().process(input_path=input_path)


if __name__ == "__main__":
    import plac

    plac.call(main)
