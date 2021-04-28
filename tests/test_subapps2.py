from fastapi.testclient import TestClient
from fastapi import FastAPI
from fastapi_offline import FastAPIOffline

# Create an application with no docs
app = FastAPI(openapi_url=None)


@app.get("/")
async def root():
    return {"message": "Hello World"}


# Create a sub-app with docs

sub_app = FastAPIOffline()


@sub_app.get("/")
async def subroot():
    return {"message": "Goodbye World"}


app.mount("/sub", sub_app)


# Create a test client
client = TestClient(app)


# Test the actual endpoints
def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_sub_main():
    response = client.get("/sub/")
    assert response.status_code == 200
    assert response.json() == {"message": "Goodbye World"}


# Check the docs pages on main are disabled
def test_disabled_docs():
    for page in ["/docs", "/redoc"]:
        response = client.get(page)
        assert response.status_code == 404


# Check the docs pages on the subapp
def test_read_docs():
    for page in ["/sub/docs", "/sub/redoc"]:
        response = client.get(page)
        assert response.status_code == 200
        assert "cdn.jsdelivr.net" not in response.text
        assert "sub/static-offline-docs" in response.text


# Check the static pages
def test_read_statics():
    for page in ["swagger-ui-bundle.js", "swagger-ui.css", "redoc.standalone.js"]:
        response = client.get("/sub/static-offline-docs/" + page)
        assert response.status_code == 200
