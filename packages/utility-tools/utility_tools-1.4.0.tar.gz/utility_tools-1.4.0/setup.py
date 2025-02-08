from setuptools import setup, find_packages

# Read README.md for the long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="utility-tools",
    version="1.4.0",  # Matching the version in UtilityTools class
    author="Good-Wizard",
    author_email="arashrahbarxz@gmail.com",  # Replace with your email
    description="A comprehensive Python utility module that provides various tools for common tasks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Good-Wizard/UtilityTools",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "qrcode>=7.3",
        "Pillow>=9.0.0",  # Required by qrcode
        "pytz>=2021.1",
        "requests>=2.26.0",
    ],
    keywords=[
        "utility",
        "tools",
        "qrcode",
        "bmi",
        "temperature",
        "password",
        "file handling",
        "compression",
        "geometry",
        "datetime",
        "http",
    ],
    project_urls={
        "Bug Reports": "https://github.com/Good-Wizard/UtilityTools/issues",
        "Source": "https://github.com/Good-Wizard/UtilityTools",
    },

    entry_points={
        "console_scripts": [
            "utility-tools=test_pypi.test:main",
        ],
    },
)
