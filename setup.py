import subprocess

from setuptools import setup

setup(
    name='gh-che',
    version='1.0.8',
    packages=['che', 'che.intercept'],
    license='LICENCE',
    author='mustafakilic',
    author_email='ben@mustafakilic.com',
    description='Long Description',
    python_requires='~=3.11',
    install_requires=[
        'mitmproxy; python_version == "3.11"',
        'click',
        'setuptools'
    ],
    package_data={
        'che': ['*.md', "*.pac", "*.json"]
    },
    entry_points={
        'console_scripts': [
            "gh-che = che.main:main"
        ]
    }

)
