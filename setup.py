from setuptools import setup

setup(
    name='ChannelWorm',
    long_description=open('README.md').read(),
    install_requires=[
        'cypy',
        'django',
        'inspyred',
        'neuronunit',
        'neurotune',
        'pillow',
        'pyelectro',
        'PyNeuroML',
        'PyOpenWorm',
        'sciunit'
    ],
    dependency_links=[
        'git+https://github.com/rgerkin/neuronunit.git#egg=neuronunit',
        'git+https://github.com/pgleeson/neurotune.git#egg=neurotune',
        'git+https://github.com/pgleeson/pyelectro.git#egg=pyelectro',
        'git+https://github.com/NeuroML/pyNeuroML.git#egg=PyNeuroML',
        'git+https://github.com/scidash/sciunit.git#egg=sciunit'
    ]
)
