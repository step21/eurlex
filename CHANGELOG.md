
# 2022-08-28

## Fixed

- Fixed importlib.metadata incompatibility

# 2022-08-28

## Changed

- Downgraded pandas to 1.3.* for compatibility with Python 3.7 and various CI and tooling fixes.

# 2022-08-24

## Added

- Initial code commit
- Added make_query and query_eurlex functions

- Added code to get notices and actual data based on celex or other identifiers.

- Added the functions for downloading and preprocessing data.
- Added missing docstrings and simmilar documentation
- Improved poetry file with reference to README

## Changed

- Changed the minimun required python version to 3.7.

- Changed minimum python version to 3.8, as 3.7 is not supported anymore by pandas.
