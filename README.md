# Project X  Frontend #
[![CircleCI](https://circleci.com/gh/vtrmantovani/project-x-front.svg?style=svg)](https://circleci.com/gh/vtrmantovani/project-x-front)
[![Coverage Status](https://coveralls.io/repos/github/vtrmantovani/project-x-front/badge.svg)](https://coveralls.io/github/vtrmantovani/project-x-front)
[![Known Vulnerabilities](https://snyk.io/test/github/vtrmantovani/project-x-front/badge.svg?targetFile=requirements.txt)](https://snyk.io/test/github/vtrmantovani/project-x-front?targetFile=requirements.txt)

This project is the frontend for project-x-api

## Dependencies
 - [Python 3.6](https://www.python.org/downloads/)
 
## Install dependencies

 1. Create one  virtualenv with python 3.6:
    ```
    virtualenv -p python3.6 env
    ```
 2. Install Python dependencies:
    ```
    make requirements-dev
    ```

## Run on development environment

### Run the api

```
make run
```


## Run the tests

```
make test
```

## Run the coverage

```
make coverage
```