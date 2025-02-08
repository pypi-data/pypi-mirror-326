from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="ssync",
    version="1.0.0-dev",
    author="Mark",
    author_email="socialsync.software@outlook.com",
    description="A powerful Python library for automating interactions with social media platforms and integrating them with backend systems.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=find_packages(),
    install_requires=[
        "requests>=2.28.1",
        "hashlib>=1.0.1",
        "typing_extensions>=4.0.0",
        "pytest>=7.0.0",
        "flake8>=5.0.0",
        "black>=23.0.0",
        "pandas>=1.3.0",
        "aiohttp>=3.8.0",
        "cryptography>=3.0.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)