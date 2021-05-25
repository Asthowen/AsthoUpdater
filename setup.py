import setuptools

with open("README.md", "r", encoding="utf-8", errors="ignore") as f:
    long_description = f.read()

setuptools.setup(
    name="AsthoUpdater",
    version="0.2.3",
    author="Asthowen",
    description="A useless asynchronous lib to update files.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Asthowen/AsthoUpdater",
    packages=setuptools.find_packages(),
    python_requires='>= 3.6',
    include_package_data=True,
    install_requires=['aiohttp', 'async-timeout']
)
