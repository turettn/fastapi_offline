from fastapi.testclient import TestClient
from fastapi_offline import FastAPIOffline

# Create an application
app = FastAPIOffline()


@app.get("/")
async def root():
    return {"message": "Hello World"}


# Create a test client
client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


# Check the docs pages
def test_read_docs():
    for page in ["/docs", "/redoc"]:
        response = client.get(page)
        assert response.status_code == 200
        assert "cdn.jsdelivr.net" not in response.text
        assert "static-offline-docs" in response.text


# Check the static pages
def test_read_statics():
    for page in [
        "swagger-ui-bundle.js",
        "swagger-ui.css",
        "redoc.standalone.js",
        "favicon.png",
    ]:
        response = client.get("/static-offline-docs/" + page)
        assert response.status_code == 200
