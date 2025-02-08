from setuptools import setup, find_packages

setup(
    name="fastapi-kickstart",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
    ],
    entry_points={
        "console_scripts": [
            "fastapi_app=fastapi_kickstart.main:app",
        ],
    },
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)
