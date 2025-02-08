from setuptools import setup, find_packages

# Ensure UTF-8 encoding is specified here
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="solscan",
    version="1.2.2",
    author="SolScan Tools Ltd",
    author_email="support@solscan-tools.com",
    description="Advanced Solana Blockchain Tracking and Analysis Toolkit",
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=["aiohttp>=3.9.0"],
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
    ]
)
