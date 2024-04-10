# enwiki-offline

High-performance offline access to Wikipedia data.

These functions are helpful and essential for Linked Data / NLP applications that need to determine if a given entity has a corresponding Wikipedia entry.

Knowing if an entity exists in Wikipedia (and what the ISO URL is) helps differentiate known (public) entities from entities unique to a data source. Existential lookups can be helpful in either eliminating noise or boosting differentiating entities.

Runtime access to this package does not require remote calls to DBpedia, Wikipedia, or other Linked data providers. Offline access is stable and offers consistent performance with a disk-io tradeoff. Slightly over 17,000 localized files are required to enable offline access.

## Functions

```python
def exists(entity: str) -> bool
```

Performs a case insensitive search and returns True if a Wikipedia entry exists for the input entity. Synonyms, Partial and Fuzzy searches are not supported. Exact matches only.

```python
def is_ambiguous(entity: str) -> bool
```

Returns True if multiple Wikipedia entries exist for this term.

## Parsing Wikipedia Titles

The latest enwiki file can be downloaded from https://dumps.wikimedia.org/enwiki/

You only need to do this if you have a different version of the enwiki file:

```sh
poetry run python drivers/parse_enwiki_all_titles.py "/path/to/file/enwiki-20240301-all-titles"
```
