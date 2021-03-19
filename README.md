# Overview

[FastAPI](https://fastapi.tiangolo.com/) is awesome, but the documentation pages (Swagger or Redoc) all depend on external CDNs, which is problematic if you want to run on disconnected networks.

This package includes the required files from the CDN and serves them locally.  It also provides a super-simple way to get a FastAPI instance configured to use those files.

Under the hood, this simply automates the process described in the official documentation [here](https://fastapi.tiangolo.com/advanced/extending-openapi/#self-hosting-javascript-and-css-for-docs).

# Installation

You can install this package from PyPi:

```bash
pip install fastapi-offline
```

# Example

Given the example from the [FastAPI tutorial](https://fastapi.tiangolo.com/tutorial/first-steps/):

```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}
```

Simply create a `fastapi_offline.FastAPIOffline` object instead:

```python
from fastapi_offline import FastAPIOffline

app = FastAPIOffline()


@app.get("/")
async def root():
    return {"message": "Hello World"}
```

Any options passed to FastAPIOffline() except `docs_url` and `redoc_url` are passed through to FastAPI.

# Licensing

* This code is released under the MIT license.
* Parts of Swagger are included in this package.  The original license ([Apache 2.0](https://swagger.io/license/)) and copyright apply to those files.
* Parts of Redoc are included in this package.  The original license ([MIT](https://github.com/Redocly/redoc/blob/master/LICENSE)) and copyright apply to those files.