from setuptools import setup, find_packages

setup(
    name="aws-dynamodb-operations",
    version="0.1.0",
    author="Msizi Gumede",
    author_email="msizi@cyberneticbg.com",
    description="A Python package for common AWS DynamoDB operations",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/MsiziGCBG/aws-dynamodb-operations",  # Update with your GitHub repo
    packages=find_packages(),
    install_requires=["boto3"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
