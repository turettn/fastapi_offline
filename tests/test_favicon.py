from fastapi.testclient import TestClient
from fastapi_offline import FastAPIOffline

# Create an application
app1 = FastAPIOffline()
client1 = TestClient(app1)

FAVICON = "http://fake.site/favicon.png"
app2 = FastAPIOffline(favicon_url=FAVICON)
client2 = TestClient(app2)

app2.mount("/app1", app1)

app3 = FastAPIOffline(favicon_url=None)
client3 = TestClient(app3)


def test_normal_redoc():
    resp = client1.get("/redoc")
    assert "/static-offline-docs/favicon.png" in resp.text


def test_custom_redoc():
    resp = client2.get("/redoc")
    assert FAVICON in resp.text


def test_normal_swagger():
    resp = client1.get("/docs")
    assert "/static-offline-docs/favicon.png" in resp.text


def test_custom_swagger():
    resp = client2.get("/docs")
    assert FAVICON in resp.text


def test_normal_submounted_redoc():
    resp = client2.get("/app1/redoc")
    print(resp.text)
    assert "/app1/static-offline-docs/favicon.png" in resp.text


def test_normal_submounted_swagger():
    resp = client2.get("/app1/docs")
    assert "/app1/static-offline-docs/favicon.png" in resp.text
