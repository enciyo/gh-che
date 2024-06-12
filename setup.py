import os

from setuptools import setup

properties = os.path.join(os.path.dirname(__file__), 'che', 'che.properties')
with open(properties) as f:
    properties = f.readlines()
prop_version = [line for line in properties if line.startswith("version")][0].split("=")[1].strip()
prop_python = [line for line in properties if line.startswith("python")][0].split("=")[1].strip()

setup(
    name='gh-che',
    version=prop_version,
    packages=['che', 'che.intercept'],
    license='LICENCE',
    author='mustafakilic',
    author_email='ben@mustafakilic.com',
    description='Chat History Exporter',
    python_requires=f'~={prop_python}',
    install_requires=[
        f'mitmproxy; python_version == "{prop_python}"',
        'click',
        'setuptools'
    ],
    package_data={
        'che': ['*.md', "*.pac", "*.json", "*.properties"]
    },
    entry_points={
        'console_scripts': [
            "gh-che = che.main:main"
        ]
    }

)
