# -*- coding: utf-8 -*-
""" Parse the EnWiki all-titles File """


import logging
from functools import lru_cache
from typing import List, Optional

from enwiki_offline.utils import (calculate_md5, exists, exists_or_error, join,
                                  join_cwd, read_json, read_string)

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class EnwikiOfflineAPI(object):

    def __init__(self):
        """ Change Log

        Created:
            9-Apr-2024
            craigtrim@gmail.com
            *   https://github.com/craigtrim/enwiki-offline/issues/1
        """
        self._output_path = join_cwd('resources/enwiki')
        exists_or_error(self._output_path)

    # @lru_cache(maxsize=5192)
    # def _get_file(self, entity: str) -> Optional[dict]:

    #     ch_path = join(self._output_path, entity[0], entity[:2])
    #     if not exists(ch_path):
    #         return None

    #     file_path = join(ch_path, f"{entity[:3]}.json")
    #     if not exists(file_path):
    #         return None

    #     return read_json(file_path)

    @lru_cache(maxsize=256)  # 16^2 variations
    def _read_file(self, prefix: str) -> None:
        """
        Writes the given dictionary `d` to a JSON file with the name `ch2` in the appropriate directory.

        Args:
            ch2 (str): The name of the file to be written.
            d (dict): The dictionary to be written to the file.

        Returns:
            None
        """

        def read(file_type: str) -> List[str]:
            ch_path = join(self._output_path, file_type)
            if not exists(ch_path):
                return None
            file_path = join(ch_path, f"{prefix}.txt")
            return read_string(file_path).split(' ')

        return read('ambiguous'), read('unambiguous')

    @lru_cache(maxsize=2048, typed=False)
    def exists(self, entity: str) -> bool:
        """
        Checks if a Wikipedia entry exists for the specified entity by performing
        a case-insensitive search within a predefined file or database. This method
        is designed to identify exact matches only; synonyms, partial matches, and
        fuzzy searches are not supported. The search is strictly limited to entities
        that exactly match the provided string, disregarding any case differences.

        The method first processes the input entity by converting it to lowercase
        and stripping any leading or trailing whitespace to standardize the input
        for comparison. It then performs the existence check based on this processed
        entity string.

        Parameters:
        - entity (str): The name of the entity for which the Wikipedia entry existence
        check is to be performed. The search is case-insensitive, but exact matching
        is required.

        Returns:
        - bool: Returns True if an exact match for the Wikipedia entry is found; otherwise,
        returns False. The method also returns False if the processed entity string
        is less than 4 characters long, under the assumption that valid Wikipedia entries
        are unlikely to be represented by such short strings.
        """
        entity = entity.lower().strip()
        if len(entity) < 4:
            return False

        md5 = calculate_md5(entity)
        ambiguous, unambiguous = self._read_file(md5[:2])

        if entity in ambiguous:
            return True

        return md5[2:] in unambiguous

    @lru_cache(maxsize=2048, typed=False)
    def is_ambiguous(self, entity: str) -> bool:
        """
        Determines if the specified entity is associated with multiple Wikipedia entries,
        indicating that the term is ambiguous. This method relies on an initial check
        to ascertain the existence of at least one Wikipedia entry for the entity. If such
        an entry exists, it further checks whether the number of entries exceeds one,
        which would classify the entity as ambiguous.

        The ambiguity check is based on the assumption that if multiple entries are
        associated with the same term, users or automated processes may require additional
        context or disambiguation to select the appropriate entry.

        Parameters:
        - entity (str): The name of the entity to check for ambiguity. This entity is
        checked against a collection of Wikipedia entries to determine if multiple
        entries exist for the same term.

        Returns:
        - bool: Returns True if the entity is associated with multiple Wikipedia entries,
        indicating ambiguity. If the entity does not exist or is associated with a single
        entry only, the method returns False.
        """

        entity = entity.lower().strip()
        if len(entity) < 4:
            return False

        md5 = calculate_md5(entity)
        ambiguous, _ = self._read_file(md5[:2])
        return md5[2:] in ambiguous
