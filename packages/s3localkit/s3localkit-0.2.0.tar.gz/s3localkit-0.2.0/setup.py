from setuptools import setup, find_packages

setup(
    name='s3localkit',
    version='0.2.0',
    packages=find_packages(),
    install_requires=[
        'boto3',
    ],
    entry_points={
        'console_scripts': [],
    },
)