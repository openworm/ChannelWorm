from setuptools import setup, find_packages

setup(
    name='ChannelWorm',
    version='0.1',
    packages=find_packages(),
    long_description=open('README.md').read(),
    install_requires=[
        'unicodecsv',
        'pillow',
        'pytest',
        'pytest-django',
        'django',
        'django-formtools',
        'django-sql-explorer',
    ]
)
