from pathlib import Path
from urllib.request import urlretrieve
from setuptools import setup
from setuptools.command.sdist import sdist


__version__ = "1.3.1"


BASE_PATH = Path(__file__).parent
README = (BASE_PATH / "README.md").read_text()


class SDistWrapper(sdist):
    def run(self) -> None:
        "Download files into static/, then pass through to normal install"
        from fastapi_offline.consts import SWAGGER_JS, SWAGGER_CSS, REDOC_JS, FAVICON

        # Find ourself

        static_path = BASE_PATH / "fastapi_offline" / "static"
        static_path.mkdir(exist_ok=True)

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
    package_data={"fastapi_offline": ["static/*"]},
    python_requires=">=3.6",
    install_requires=["aiofiles", "fastapi"],
    tests_require=["pytest", "requests"],
    setup_requires=["fastapi", "aiofiles"],
    cmdclass={"sdist": SDistWrapper},
)
