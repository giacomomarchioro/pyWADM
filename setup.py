import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyWADM",
    version="0.0.1",
    author="Giacomo Marchioro",
    author_email="giacomomarchioro@outlook.com",
    description="A tool for easing the construction of JSON object compliant with the Web Annotation Data Model",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/giacomomarchioro/pyWADM",
    packages=setuptools.find_packages(),
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
