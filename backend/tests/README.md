# Unit tests for backend FastAPI microservice

This file contains unit tests for FastAPI microservice endpoints.

To run tests simply run in terminal 

```bash
pytest
```
in this directory.

If you want to store logs in seperate file, use `>` operator. Example of storing logs in `test_logs` file:

```bash
pytest -rA -v > test_logs
```

`pytest` is a python package so you can install it from PyPi repository with `pip` package manager:

```bash
pip install pytest
```

