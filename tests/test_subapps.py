from fastapi.testclient import TestClient
from fastapi import FastAPI
from fastapi_offline import FastAPIOffline

# Create an application with docs
app = FastAPIOffline()


@app.get("/")
async def root():
    return {"message": "Hello World"}


# Create a sub-application with no docs
subapp_no_docs = FastAPI(openapi_url=None)


@subapp_no_docs.get("/")
async def sub_root():
    return {"message": "Goodbye World"}


app.mount("/sub_no_docs", subapp_no_docs)

# Create a sub-application with docs
subapp_yes_docs = FastAPIOffline()


@subapp_yes_docs.get("/")
async def sub2_root():
    return {"message": "Congrats World"}


app.mount("/sub_yes_docs", subapp_yes_docs)

# Create a test client
client = TestClient(app)

# Check the main app still works
def test_read_main():
    """Hello World"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


# Test the sub apps work
def test_sub_app():
    """Goodbye World"""
    response = client.get("/sub_no_docs/")
    assert response.status_code == 200
    assert response.json() == {"message": "Goodbye World"}


def test_sub2_app():
    """Congrats World"""
    response = client.get("/sub_yes_docs/")
    assert response.status_code == 200
    assert response.json() == {"message": "Congrats World"}


# Check the docs pages on the main app
def test_read_docs():
    for page in ["/docs", "/redoc"]:
        response = client.get(page)
        assert response.status_code == 200
        assert "cdn.jsdelivr.net" not in response.text
        assert "static-offline-docs" in response.text


# Check the static pages on the main app
def test_read_statics():
    for page in ["swagger-ui-bundle.js", "swagger-ui.css", "redoc.standalone.js"]:
        response = client.get("/static-offline-docs/" + page)
        assert response.status_code == 200


# Make sure that the first subapp doesn't have docs
def test_subapp_no_docs():
    response = client.get("/sub_no_docs/docs")
    assert response.status_code == 404


# Make sure the second does
def test_subapp_yes_docs():
    for page in ["sub_yes_docs/docs", "sub_yes_docs/redoc"]:
        response = client.get(page)
        assert response.status_code == 200
        assert "cdn.jsdelivr.net" not in response.text
        assert "sub_yes_docs/static-offline-docs" in response.text
