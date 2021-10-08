import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="LeadsRx_Python_Client",
    version="0.0.9",
    author="Josh Hatfield",
    author_email="jh@semetrical.com",
    description="A python client for querying the LeadsRX API. Created in my spare time to help out Semetricals Analytics Team",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JoshHatfield/LeadsRx-Python-Client",
    project_urls={
        "Bug Tracker": "https://github.com/JoshHatfield/LeadsRx-Python-Client/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=['requests>=2.25.1','pandas>=1.1.5']
)