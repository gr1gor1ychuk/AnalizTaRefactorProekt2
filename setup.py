from setuptools import setup, find_packages

setup(
    name="sport-equipment-store",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "fastapi==0.109.2",
        "uvicorn==0.27.1",
        "pytest==8.0.0",
        "pytest-cov==4.1.0",
        "httpx==0.26.0",
        "python-multipart==0.0.9"
    ],
) 