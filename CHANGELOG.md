# Change Log

## Version 0.2.2

* Add typing support

## Version 0.2.1

* Correct exception properties
* [black](https://github.com/ambv/black) formatting

## Version 0.2.0

* Change to using named parameters in most cases
* Ensure all keys are handled correctly in response

## Version 0.1.0

* Added `timeout` property
* Added ability to pull all episodes when pulling a series (optional)
* `strict` property allows for swallowing exceptions
* Use __slots__

## Version 0.0.4

* Search pulls all results unless specified not to do so
* Added additional exceptions
  * OMDBTooManyResults
  * OMDBInvalidAPIKey
* Added ability to set the API key
* Convert dictionary from camelCase to snake_case

## Version 0.0.3

* Added doc strings for online documentation and deployed to [readthedocs.org](https://pyomdbapi.readthedocs.io/en/latest/)
* Fixed a call to the formatting of results

## Version 0.0.2

* Fixed error with formatting the results

## Version 0.0.1

* Initial Release
  * Search by movie or series name
  * Get movie, series, or episode by name or IMDBid
