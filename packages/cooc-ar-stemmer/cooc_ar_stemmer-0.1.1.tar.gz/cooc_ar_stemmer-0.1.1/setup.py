from setuptools import setup, find_packages

setup(
    name="cooc_ar_stemmer",
    version="0.1.1",
    author="Iskander Akhmetov",
    author_email="iskander.akhmetov@gmail.com",
    description="A stemmer for the Arabic language",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/iskander-akhmetov/cooc_ar_stemmer",
    packages=find_packages(),
    include_package_data=False,  # Prevent auto-inclusion of LICENSE.txt
    package_data={"cooc_ar_stemmer": ["mx.pkl", "dic.pkl", "vectorizer.pkl"]},  # Ensure structured data
    license="Proprietary",  # Set license properly
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11.7",
)
