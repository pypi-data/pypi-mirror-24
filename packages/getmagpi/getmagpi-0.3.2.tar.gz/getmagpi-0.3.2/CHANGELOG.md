# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [Unreleased]
- .magignore file
- Logging

## [0.3.2] - 2018-09-05
### Changed
- fixes to setup.py
- clone readme for PyPi

## [0.3.1] - 2017-09-04
### Fixed
- setup.py and packaging 

## [0.3.0] - 2017-09-03
### Changed
- Switched to BeautifulSoup for HTML parsing.  (Original experiment was to be Standard Library-only.  Troublesome across Python versions.)

## [0.2.2] - 2017-08-10
### Fixed
- Fix packaging bug

## [0.2.1] - 2017-08-06
### Added
- restructured text README for PyPi

## [0.2.0] - 2017-08-06
### Changed
- Moved Standard Library URL handling to 'requests'
- Refactors to support common Python 2/3

### Added
- setup.py for local install and pypi

## [0.1.0] - 2017-08-05
### Added
- HTML parser for remote file listing.
- Filesystem handler for local PDF library.
- Handler for deltas between Source and Target librarys ('--compare').
- Switch for non-English files (uses file description terms).
- Standard-Library file downloader.
- Create README.
- Add LICENSE.
- Create this CHANGELOG.