from setuptools import setup

setup(
    name='ChannelWorm',
    long_description=open('README.md').read(),
    install_requires=[
        'PyNeuroML',
        'PyOpenWorm',
        'cypy',
        'django',
        'django-formtools',
        'django-sql-explorer',
        'inspyred',
        'neurotune',
        'pillow',
        'pyelectro',
        'sciunit',
    ],
    dependency_links=[
        'git+https://github.com/scidash/sciunit.git#egg=sciunit',
        'git+https://github.com/openworm/PyOpenWorm.git#egg=PyOpenWorm',
        'git+https://github.com/NeuroML/pyNeuroML.git#egg=PyNeuroML',
        'git+https://github.com/pgleeson/pyelectro.git#egg=pyelectro',
        'git+https://github.com/pgleeson/neurotune.git#egg=neurotune'
    ]
)
