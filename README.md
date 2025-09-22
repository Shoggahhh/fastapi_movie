# FastAPI Url Shortener

[![Python checks 🐍](https://github.com/Shoggahhh/fastapi_movie/actions/workflows/python-checks.yaml/badge.svg?branch=master)](https://github.com/Shoggahhh/fastapi_movie/actions/workflows/python-checks.yaml)

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
