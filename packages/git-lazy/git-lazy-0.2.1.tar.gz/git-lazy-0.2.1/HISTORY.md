# History
All notable changes to this project will be documented in this file. This project adheres to [Semantic Versioning](http://semver.org/).

## 0.1.0 (2016-03-01)
* First release on PyPI.

## 0.1.1 (2016-03-04)
* Do not attempt to do git operations on non-existent repos on current machine.

## 0.1.5 (2017-02-21)
* Various enhancements

## 0.1.7 (2017-04-04)
* Bug fix where using `--find` after already using it would only create a repo list of the newly found repos.

## 0.1.8 (2017-04-24)
* Bug fix where using `--find` would add repos twice.

## 0.1.9 (2017-06-25)
* Added `--update_origins` to update all repo urls from HTTPS to SSH

## 0.2.0 (2017-08-04)
* Fixed bug with `--find`

## 0.2.1 (2017-08-04)
* Fixed bug with `--find` when no origin set
* Update `update_origins` regex logic to handle https and ssh schemes
* Added `repo_users` to config (comma-delimited)
