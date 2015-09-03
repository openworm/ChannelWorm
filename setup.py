from setuptools import setup

setup(
    name='ChannelWorm',
    packages=[
        'channelworm',
        'channelworm.ion_channel',
        'channelworm.digitizer',
        'channelworm.web_app',
        'channelworm.fitter'
    ],
    long_description=open('README.md').read(),
    install_requires=[
        'cypy',
        'Django<=1.8',
        'django-formtools',
        'django-sql-explorer',
        'inspyred',
        'neuronunit',
        'numpy',
        'pillow',
        'pytest',
        'pytest-django',
        'quantities',
        'sciunit>=0.1.3.2',
    ]
)
