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
        'inspyred',
        'sqlparse',
        'python-unicodecsv',
        'pillow',
        'pytest',
        'pytest-django',
    ]
)
