from setuptools import setup

setup(
    name='ChannelWorm',
    packages=[
        'channelworm',
        'channelworm.ion_channel',
        'channelworm.digitizer',
        'channelworm.account',
        'channelworm.web_app',
        'channelworm.fitter',
        'channelworm.predictor'
    ],
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
