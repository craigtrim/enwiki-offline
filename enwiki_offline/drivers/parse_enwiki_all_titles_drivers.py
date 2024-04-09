# -*- coding: utf-8 -*-
""" Parse the EnWiki all-titles File """


from enwiki_offline.parser.bp import ParseEnwikiAllTitles


def main(input_path):
    ParseEnwikiAllTitles().process(input_path)


if __name__ == "__main__":
    import plac

    plac.call(main)
