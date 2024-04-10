#!/usr/bin/env python
# -*- coding: UTF-8 -*-


import os
from codecs import open as codecs_open
from hashlib import md5
from json import load as json_load


def join_cwd(*args) -> str:
    return os.path.normpath(os.path.join(os.getcwd(), *args))


def join(*args) -> str:
    return os.path.normpath(os.path.join(*args))


def exists_or_error(file_path: str) -> None:
    """ Raise Exception if File Path does not exist

    Args:
        file_path (str): an input path

    Raises:
        FileNotFoundError: an input path
    """
    if not exists(file_path):
        raise FileNotFoundError(file_path)


def exists(file_path: str) -> bool:
    """ Check if File or Directory exists

    Args:
        file_path (str): a file path

    Returns:
        bool: True if file or directory exists
    """
    return os.path.exists(file_path)


def read_json(file_path: str) -> object:
    """ Read JSON from File

    Args:
        file_path (str): the absolute and qualified output file path
        file_encoding (str, optional): The output file encoding. Defaults to "utf-8".

    Returns:
        [type]: the JSON object
    """
    with open(file_path) as json_file:
        return json_load(json_file)


def exists_or_create(file_path: str) -> None:
    """ Create File Path if File Path does not exist

    Args:
        file_path (str): an input path
    """
    if not exists(file_path):
        create_dir(file_path)


def create_dir(dir_name: str) -> None:
    """ Create Directory (recursive)

    Args:
        dir_name (str): an input path
    """
    if not os.path.isdir(dir_name):
        os.makedirs(dir_name)


def write_string(input_text: str,
                 file_path: str,
                 file_encoding: str = 'utf-8') -> None:
    """ Write String to File

    Args:
        input_text (str): the string contents to write to file
        file_path (str): the absolute and qualified input file path
        file_encoding (str, optional): the file encoding. Defaults to "utf-8".

    Raises:
        ValueError: Invalid Input
    """
    if not input_text or not isinstance(input_text, str):
        raise ValueError

    target = codecs_open(file_path, mode='w', encoding=file_encoding)
    target.write(input_text)
    target.close()


def read_string(file_path: str) -> str:
    """
    Reads the contents of a file and returns it as a string.

    Args:
        file_path (str): The path to the file to be read.

    Returns:
        str: The contents of the file as a string.
    """
    with open(file_path, 'r') as file:
        return ''.join(file.readlines())


def calculate_md5(input_text: str) -> str:
    """
    Generate an MD5 hash from the provided input string.

    The MD5 hashing algorithm is used here to produce a 128-bit hash value
    from the input string. While MD5 is fast and has been popular in the past,
    it's worth noting that there are cryptographic vulnerabilities associated
    with it, making it less suitable for security-sensitive applications today.

    Args:
        input_text (str): The input string that needs to be hashed.

    Returns:
        str: The MD5 hash of the input string in hexadecimal format.

    Usage:
        >>> calculate_md5("Hello, World!")
        'fc3ff98e8c6a0d3087d515c0473f8677'

    Notes:
        The function utilizes Python's built-in hashlib library. There are
        alternate methods to achieve the same, including using a bytestream
        method. However, for hashing strings, direct use of hashlib is more
        efficient.
    """

    # Using hashlib to compute MD5 hash directly from the input string.
    return md5(input_text.encode()).hexdigest()
