from setuptools import setup

setup(
    name='gh-che',
    version='3.0.1',
    packages=['che', 'che.intercept'],
    license='LICENCE',
    author='mustafakilic',
    author_email='ben@mustafakilic.com',
    description='Long Description',
    requires_python='>=3.11',
    install_requires=[
        'mitmproxy~=10.3.0',
        'click',
        'setuptools'
    ],
    package_data={
        'che': ['sample.md']
    },
    entry_points={
        'console_scripts': [
            "gh-che = che.main:main"
        ]
    }

)
