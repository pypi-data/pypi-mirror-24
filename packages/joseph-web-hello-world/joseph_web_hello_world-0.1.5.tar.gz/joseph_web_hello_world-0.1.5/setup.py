from setuptools import setup

__VERSION__ = "0.1.5"


setup(
    name="joseph_web_hello_world",
    description="A basic HTTP handler for Joseph.",
    author="Niek Keijzer",
    author_email="info@niekkeijzer.com",
    url="https://github.com/NiekKeijzer/HTTPTest",
    download_url="https://github.com/NiekKeijzer/HTTPTest/archive/{}.tar.gaz".format(__VERSION__),
    keywords=[
        "http",
        "web",
        "hello_world"
        "joseph"
    ],
    packages=[
        "joseph_web"
    ],
    version=__VERSION__,
    entry_points={
        'joseph.http': [
            '(GET)/test = joseph_web.handlers:index'
        ]
    }
)