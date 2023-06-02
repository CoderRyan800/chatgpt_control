from setuptools import setup, find_packages

setup(
    name="chatgpt_control",
    version="0.1",
    packages=find_packages() + ["code"],
    install_requires=[
        "mysql-connector-python",
        "openai"
    ],
    package_data={
        "config": ["config.json"],
    }
    # ...
)
