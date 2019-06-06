import setuptools

with open("README.md", "r") as fd:
    long_description = fd.read()

setuptools.setup(
    name="expr",
    version="1.0.0",
    author="Julien Castiaux",
    author_email="julien.castiaux@gmail.com",
    description="A simple engine built to compute logical, bitwise and arithmetic expressions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Julien00859/expr",
    packages=setuptools.find_packages(),
    install_requires=["lark-parser"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Text Processing",
    ],
)
