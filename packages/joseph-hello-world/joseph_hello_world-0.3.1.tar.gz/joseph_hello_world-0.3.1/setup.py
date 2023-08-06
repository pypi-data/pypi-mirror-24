from setuptools import setup

__VERSION__ = "0.3.1"


setup(
    name="joseph_hello_world",
    description="A hello world plugin for Joseph. Write an hello world message to the logs.",
    author="Niek Keijzer",
    author_email="info@niekkeijzer.com",
    url="https://github.com/NiekKeijzer/HelloWorld",
    download_url="https://github.com/NiekKeijzer/HelloWorld/archive/{}.tar.gaz".format(__VERSION__),
    keywords=[
        "hello world",
        "joseph"
    ],
    packages=[
        "hello_world"
    ],
    version=__VERSION__,
    entry_points={
        'joseph.actions': [
            'say_hello = hello_world.hello:say_hello'
        ]
    }
)