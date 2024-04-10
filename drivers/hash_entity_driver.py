# -*- coding: utf-8 -*-
""" Parse the EnWiki all-titles File """


from collections import defaultdict
from copy import deepcopy
from json import dump
from typing import Iterator, List

from baseblock import BaseObject, Stopwatch

from enwiki_offline.utils import (calculate_md5, exists, exists_or_create,
                                  exists_or_error, join, join_cwd, read_string,
                                  write_string)


def main(entity):
    md5 = calculate_md5(entity)
    print(md5)

    def exists(type: str) -> bool:

        input_path: str = join_cwd(f'resources/enwiki/{type}')
        exists_or_error(input_path)

        input_file: str = join(input_path, f"{md5[:2]}.txt")
        exists_or_error(input_file)

        contents = read_string(input_file)
        return md5[2:] in contents

    print(f"Ambiguous: {exists('ambiguous')}")
    print(f"Unambiguous: {exists('unambiguous')}")


if __name__ == "__main__":
    import plac

    plac.call(main)
