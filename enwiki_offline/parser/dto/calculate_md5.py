#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from hashlib import md5


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
