from setuptools import setup

name = "types-dateparser"
description = "Typing stubs for dateparser"
long_description = '''
## Typing stubs for dateparser

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`dateparser`](https://github.com/scrapinghub/dateparser) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
[Pyre](https://pyre-check.org/),
PyCharm, etc. to check code that uses `dateparser`. This version of
`types-dateparser` aims to provide accurate annotations for
`dateparser==1.2.*`.

This package is part of the [typeshed project](https://github.com/python/typeshed).
All fixes for types and metadata should be contributed there.
See [the README](https://github.com/python/typeshed/blob/main/README.md)
for more details. The source for this package can be found in the
[`stubs/dateparser`](https://github.com/python/typeshed/tree/main/stubs/dateparser)
directory.

This package was tested with
mypy 1.15.0,
pyright 1.1.389,
and pytype 2024.10.11.
It was generated from typeshed commit
[`73ebb9dfd7dfce93c5becde4dcdd51d5626853b8`](https://github.com/python/typeshed/commit/73ebb9dfd7dfce93c5becde4dcdd51d5626853b8).
'''.lstrip()

setup(name=name,
      version="1.2.0.20250208",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/dateparser.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['dateparser_data-stubs', 'dateparser-stubs'],
      package_data={'dateparser_data-stubs': ['__init__.pyi', 'settings.pyi', 'METADATA.toml', 'py.typed'], 'dateparser-stubs': ['__init__.pyi', 'calendars/__init__.pyi', 'calendars/hijri.pyi', 'calendars/hijri_parser.pyi', 'calendars/jalali.pyi', 'calendars/jalali_parser.pyi', 'conf.pyi', 'custom_language_detection/__init__.pyi', 'custom_language_detection/fasttext.pyi', 'custom_language_detection/langdetect.pyi', 'custom_language_detection/language_mapping.pyi', 'data/__init__.pyi', 'data/languages_info.pyi', 'date.pyi', 'date_parser.pyi', 'freshness_date_parser.pyi', 'languages/__init__.pyi', 'languages/dictionary.pyi', 'languages/loader.pyi', 'languages/locale.pyi', 'languages/validation.pyi', 'parser.pyi', 'search/__init__.pyi', 'search/detection.pyi', 'search/search.pyi', 'search/text_detection.pyi', 'timezone_parser.pyi', 'timezones.pyi', 'utils/__init__.pyi', 'utils/strptime.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0",
      python_requires=">=3.9",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
