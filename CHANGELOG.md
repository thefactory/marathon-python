## 0.5.0 (2014-09-15)

Initial release compatible with Marathon 0.7.0 and Mesos 0.20.0.

_Warning: this includes multiple breaking changes, both from Marathon and from this library_

Changes:
* Added support for Deployments, Groups, native Docker containers, Queue, Server Info, Server Metrics, and Ping
* Updated object attributes to be at parity with Marathon 0.7.0 (RC2)
* Updated return types to be at parity with Marathon 0.7.0 (RC2)
* Updated method signatures to be more consistent
* HTTP 4xx errors other than 404 now through `MarathonHttpError` instead of `NotFoundError`
* `json_encode()` and `json_decode()` on MarathonResource have been renamed to `to_json()` and `from_json()`, respectively
* Refactored serialization/deserialization to reduce boilerplate
