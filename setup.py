from pathlib import Path
from urllib.request import build_opener, install_opener, urlretrieve

from setuptools import setup
from setuptools.command.sdist import sdist

__version__ = "1.7.4"


BASE_PATH = Path(__file__).parent
README = (BASE_PATH / "README.md").read_text()
FASTAPI_VER = "fastapi>=0.99.0"
TEST_DEPS = ["pytest", "requests", "starlette[full]"]


class SDistWrapper(sdist):
    def run(self) -> None:
        "Download files into static/, then pass through to normal install"
        from fastapi_offline.consts import FAVICON, REDOC_JS, SWAGGER_CSS, SWAGGER_JS

        # Find ourself

        static_path = BASE_PATH / "fastapi_offline" / "static"
        static_path.mkdir(exist_ok=True)

        # Set a header to avoid cloudflare's bot blocker
        opener = build_opener()
        opener.addheaders = [
            ("User-agent", f"fastapi-offline-packager / {__version__}")
        ]
        install_opener(opener)

        # Download files
        for download in (
            SWAGGER_JS,
            SWAGGER_CSS,
            REDOC_JS,
            FAVICON,
        ):
            urlretrieve(download, static_path / download.split("/")[-1])

        sdist.run(self)


setup(
    name="fastapi_offline",
    version=__version__,
    author="Neal Turett",
    author_email="turettn@gmail.com",
    description="FastAPI without reliance on CDNs for docs",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/turettn/fastapi_offline",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
    ],
    packages=["fastapi_offline"],
    package_data={"fastapi_offline": ["static/*", "py.typed"]},
    python_requires=">=3.8",
    install_requires=[FASTAPI_VER],
    tests_require=TEST_DEPS,
    setup_requires=[FASTAPI_VER],
    extras_require={"test": TEST_DEPS},
    cmdclass={"sdist": SDistWrapper},
)
