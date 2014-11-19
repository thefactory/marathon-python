## 0.6.8 (2014-11-18)

Changes:
* (Temporarily) Add `apps` field to `DeploymentAction` (https://github.com/mesosphere/marathon/pull/802)

## 0.6.7 (2014-11-18)

Changes:
* Updated `list_tasks()` and `get_info()` to match latest Marathon response signature
* Fixed `__repr__` for `MarathonInfo()` and other `MarathonResources` without `id

## 0.6.6 (2014-11-17)

Changes:
* Improved behavior of `MarathonClient.update_app()` to strip `version` from the passed `app`

## 0.6.5 (2014-11-14)

Changes:
* Fixed bug with `MarathonClient.scale_app()` and add `force` support

## 0.6.4 (2014-11-13)

Support for Marathon 0.7.5

Changes:
* Added support for app.lastTaskFailure
* Added support for task.healthCheckResult
* Fixed support for app.upgradeStrategy

## 0.6.3 (2014-10-10)

Changes:
* Added support for embedding tasks in get/list app results
* Switched to patch-style updates for apps and groups (send partial object)

## 0.6.2 (2014-10-09)

Changes:
* Added support for service port in container port mappings (Marathon 0.7.3)

## 0.6.2 (2014-10-09)

Changes:
* Added support for LIKE and UNLIKE constraint operators
* Added support for patch-style app and group updates

## 0.6.1 (2014-09-29)

Changes:
* Fixed broken exception import

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
