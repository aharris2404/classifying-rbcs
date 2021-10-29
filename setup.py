import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rbc-classifier",
    version="0.0.1",
    author="Anton Nekhai",
    author_email="nekhai.anton@gmail.com",
    description="A package to classify red blood cells from sickle cells",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aharris2404/classifying-rbcs",
    project_urls={
        "Bug Tracker": "https://github.com/aharris2404/classifying-rbcs/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
#        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)