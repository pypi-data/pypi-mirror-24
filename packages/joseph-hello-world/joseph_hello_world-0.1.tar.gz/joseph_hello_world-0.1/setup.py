from setuptools import setup


setup(
    name="joseph_hello_world",
    description="A hello world plugin for Joseph",
    author="Niek Keijzer",
    author_email="info@niekkeijzer.com",
    url="https://github.com/NiekKeijzer/HelloWorld",
    download_url="https://github.com/NiekKeijzer/HelloWorld/archive/0.1.tar.gaz",
    keywords=[
        "hello world",
        "joseph"
    ],
    packages=[
        "hello_world"
    ],
    version="0.1",
    entry_points={
        'joseph.plugins': 'hello = src:hello'
    }
)