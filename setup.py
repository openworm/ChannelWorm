from setuptools import setup

setup(
    name='ChannelWorm',
    long_description=open('README.md').read(),
    install_requires=[
        'cypy',
        'sciunit',
        'PyOpenWorm',
        'PyNeuroML>=0.0.6'
    ],
    dependency_links=[
        'git+https://github.com/scidash/sciunit.git#egg=sciunit',
        'git+https://github.com/openworm/PyOpenWorm.git#egg=PyOpenWorm',
        'git+https://github.com/NeuroML/pyNeuroML.git#egg=PyNeuroML@5aeab1243567d9f4a8ce16516074dc7b93dfbf37'
    ]
)
