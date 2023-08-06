from setuptools import setup

__VERSION__ = "0.1.1"


setup(
    name="joseph_http_test",
    description="A basic HTTP handler for Joseph.",
    author="Niek Keijzer",
    author_email="info@niekkeijzer.com",
    url="https://github.com/NiekKeijzer/HTTPTest",
    download_url="https://github.com/NiekKeijzer/HTTPTest/archive/{}.tar.gaz".format(__VERSION__),
    keywords=[
        "http",
        "joseph"
    ],
    packages=[
        "http"
    ],
    version=__VERSION__,
    entry_points={
        'joseph.http': [
            '/test = http.handlers:index'
        ]
    }
)