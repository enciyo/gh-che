from setuptools import setup

setup(
    name='gh-che',
    version='3.0.0',
    packages=['che', 'che.intercept'],
    license='LICENCE',
    author='mustafakilic',
    author_email='ben@mustafakilic.com',
    description='Long Description',
    install_requires=[
        'mitmproxy~=10.3.0',
        'click',
        'setuptools'
    ],
    entry_points={
        'console_scripts': [
            "gh-che = che.main:main"
        ]
    }
)
