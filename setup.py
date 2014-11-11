from setuptools import setup, find_packages


setup(
    version='1.1',
    name='pira',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'pira=pira.cli:main'
        ]
    },
    install_requires=[
        'python-musicpd'
    ])
