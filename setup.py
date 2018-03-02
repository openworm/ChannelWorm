from setuptools import setup

setup(
    name='ChannelWorm',
    version='0.1',
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
    ]
)
