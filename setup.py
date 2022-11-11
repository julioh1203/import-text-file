from setuptools import setup

setup(
    name="import_files",
    version="0.1.0",
    packages=['import-files'],
    install_requires = [
        "django",
        "pandas",
        "python-decouple",
    ]
)
