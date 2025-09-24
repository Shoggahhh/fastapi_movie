# FastAPI Url Shortener


[![CI: Python checks 🐍](https://img.shields.io/github/actions/workflow/status/Shoggahhh/fastapi_movie/python-checks.yaml?branch=master&label=Python%20checks%20%F0%9F%90%8D&style=for-the-badge&logo=github)](https://github.com/Shoggahhh/fastapi_movie/actions/workflows/python-checks.yaml)

[![Python](https://img.shields.io/badge/python-3.13-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Code style: Black](https://img.shields.io/badge/code%20style-black-000000?style=for-the-badge)](https://github.com/psf/black)
[![Ruff](https://img.shields.io/badge/lint-ruff-F9622E?style=for-the-badge&logo=ruff&logoColor=white)](https://github.com/astral-sh/ruff)
[![mypy](https://img.shields.io/badge/types-mypy-2F74C0?style=for-the-badge&logo=mypy&logoColor=white)](https://github.com/python/mypy)
[![uv](https://img.shields.io/badge/deps%20manager-uv-222?style=for-the-badge)]([https://docs.astral.sh/uv/](https://github.com/astral-sh/uv))

[![codecov](https://codecov.io/gh/Shoggahhh/fastapi_movie/branch/master/graph/badge.svg)](https://codecov.io/gh/Shoggahhh/fastapi_movie)

## Developer

Check GitHub Action after any push

### Setup

Right click 'movie' -> Mark Directory as -> Sources Root

### Install dependencies

Install all packages:
```shell
uv sync
```

### Configure pre-commit

Install pre-commit hook:
```shell
pre-commit install
```

### Run

Go to workdir

```shell
cd movie
```

Run dev server

```shell
fastapi dev
```

## Snippets
```shell
python -c 'import secrets;print(secrets.token_urlsafe(16))'
```
