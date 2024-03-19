import setuptools

# Reads the content of your README.md into a variable to be used in the setup below
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="kylie_bee_private_shared_code",  # should match the package folder
    version="0.1.0",  # important for updates
    author="Kylie McNaughton",
    author_email="kylie@sema4.ai",
    description="Testing installation of Package",
    long_description=long_description,  # loads your README.md
    long_description_content_type="text/markdown",  # README.md is of type 'markdown'
    url="https://github.com/kylie-bee/test-private-shared-code",
    packages=["kylie_bee_private_shared_code"],  # should match the package folder
    install_requires=["robocorp==2.0.0"],  # list of dependencies
)
