
# 2022-09-03

## Added

- Extracting title, parties and case number from title data. This has to be explicitly specified and will not work on f.e. directives.

## Fixed

- Fixed get data to properly parse title data, and ids.

# 2022-09-01

## Added

- Made text output mostly only available when started from the commandline (as main)..

## Fixed

- Fixed a bug in `get_data` due to an uninitialized variable.

# 2022-08-31

## Changed

- Changed the query for dates, so that str() is not used. This allows for proper column names in pandas dataframes.

# 2022-08-30

## Added

- Added a test for a directive query.

## Fixed

- Fixed the `caselaw_proper`resource type in `make_query`.

# 2022-08-30

## Added

- Added initial proper tests, one per function.

## Changed

- Improved docstrings.

## Fixed

- Fixed pylint issues and some bugs that were recently introduced.

# 2022-08-28

## Changed

- Added Literal support for Python 3.7.

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
