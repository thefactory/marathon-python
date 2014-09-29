## 0.6.1 (2014-09-29)

Changes:
* Fix broken exception import

## 0.6.0 (2014-09-29)

Mesos 0.20.1- and Marathon 0.7.1-compatible release.

Changes:
* Added bridge networking support
* Use common exception for all pick-from-a-list options (`InvalidChoiceError`). `InvalidOperatorError` has been removed
* Updated `MarathonObject.__repr__` to be more useful
* Changed default HTTP request timeout from 5s to 10s

## 0.5.1 (2014-09-18)

Changes:
* Added support for multiple Marathon servers (if a request to one fails for network reasons, try the next)
* Fixed a bug with HTTP 4xx response handling

## 0.5.0 (2014-09-15)

Initial release compatible with Marathon 0.7.0 and Mesos 0.20.0.

_Warning: this includes multiple breaking changes, both from Marathon and from this library_

Changes:
* Added support for Deployments, Groups, native Docker containers, Queue, Server Info, Server Metrics, and Ping
* Updated object attributes to be at parity with Marathon 0.7.0 (RC2)
* Updated return types to be at parity with Marathon 0.7.0 (RC2)
* Updated method signatures to be more consistent
* HTTP 4xx errors other than 404 now throw `MarathonHttpError` instead of `NotFoundError`
* `json_encode()` and `json_decode()` on MarathonResource have been renamed to `to_json()` and `from_json()`, respectively
* Refactored serialization/deserialization to reduce boilerplate
