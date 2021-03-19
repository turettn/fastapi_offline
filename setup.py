from pathlib import Path
from urllib.request import urlretrieve
from setuptools import setup
from setuptools.command.sdist import sdist

__version__ = "1.0.0"


BASE_PATH = Path(__file__).parent
README = (BASE_PATH / "README.md").read_text()

DOWNLOADS = (
    "https://cdn.jsdelivr.net/npm/swagger-ui-dist@3/swagger-ui-bundle.js",
    "https://cdn.jsdelivr.net/npm/swagger-ui-dist@3/swagger-ui.css",
    "https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js",
)


class SDistWrapper(sdist):
    def run(self) -> None:
        "Download files into static/, then pass through to normal install"
        # Find ourself

        static_path = BASE_PATH / "fastapi_offline" / "static"
        static_path.mkdir(exist_ok=True)

        # Download files
        for download in DOWNLOADS:
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
    cmdclass={"sdist": SDistWrapper},
)
