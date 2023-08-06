import os
from distutils.core import setup

with open(os.path.join(os.path.dirname(__file__), 'VERSION'), 'r') as f:
    __version = f.read()

setup(
    name = 'dnutils',
    packages = ['dnutils'],
    version = __version,
    description = 'A collection of convenience tools for everyday Python programming',
    author = 'Daniel Nyga',
    author_email = 'daniel.nyga@t-online.de',
    url = 'https://spritinio.de/dnutils',
    download_url = 'https://github.com/danielnyga/dnutils/archive/%s.tar.gz' % __version,
    keywords = ['testing', 'logging', 'threading', 'multithreading', 'debugging', 'tools'],
    classifiers = [],
    install_requires=[
        'colored==1.3.5',
        'tabulate',
        'portalocker',
    ],
    package_data={
        '': [
            'VERSION',
        ]
    },
)