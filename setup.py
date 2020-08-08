from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

setup(
    name="strbalance",
    version="0.2.1",
    author="Tamila Krashtan",
    author_email="tamila.krashtan@gmail.com",
    description="A package to check whether a string is balanced",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/tamila-krashtan/strbalance",
    packages=find_packages(),
    python_requires='>=3',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
