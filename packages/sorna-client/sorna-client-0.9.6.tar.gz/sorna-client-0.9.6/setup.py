# Always prefer setuptools over distutils
from setuptools import setup
from os import path
import pip

here = path.abspath(path.dirname(__file__))

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except (IOError, ImportError):
    long_description = ""

requires = []
links = []
requirements = pip.req.parse_requirements(
    'requirements.txt', session=pip.download.PipSession()
)
for item in requirements:
    if getattr(item, 'url', None):  # older pip has url
        links.append(str(item.url))
    if getattr(item, 'link', None):  # newer pip has link
        links.append(str(item.link))
    if item.req:
        requires.append(str(item.req))  # always the package name


setup(
    name='sorna-client',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version='0.9.6',
    description='Sorna API Client Library',
    long_description=long_description,
    url='https://github.com/lablup/sorna-client',
    author='Lablup Inc.',
    author_email='joongi@lablup.com',
    license='LGPLv3',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Operating System :: POSIX',
        'Operating System :: MacOS :: MacOS X',
        'Environment :: No Input/Output (Daemon)',
        'Topic :: Scientific/Engineering',
        'Topic :: Software Development',
    ],

    packages=['sorna', 'sorna.asyncio'],

    python_requires='>=3.5',
    install_requires=requires,
    dependency_links=links,
    extras_require={
        'dev': ['pytest', 'pytest-cov', 'pytest-mock', 'pytest-asyncio', 'asynctest', 'codecov'],
        'test': ['pytest', 'pytest-cov', 'pytest-mock', 'pytest-asyncio', 'asynctest', 'codecov'],
    },
    data_files=[],
    entry_points={
        'console_scripts': [
            'lcc = sorna.cli:main',
            'lpython = sorna.cli:main',
        ],
    },
)
