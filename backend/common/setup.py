from setuptools import setup, find_packages

setup(
    name="smarttravel-common",
    version="0.1.0",
    package_dir={"common": "."},
    packages=["common", "common.auth", "common.models", "common.schemas", "common.utils", "common.mq"],
    install_requires=[
        "sqlalchemy>=2.0",
        "pydantic>=2.9",
        "pyjwt>=2.8",
    ],
    python_requires=">=3.12",
)