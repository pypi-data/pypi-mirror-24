from setuptools import setup
import re


def readme():
    with open('README.rst') as f:
        return f.read()


VERSIONFILE = "eobot/_version.py"
verstrline = open(VERSIONFILE, "rt").read()
VSRE = r"^__version__\s+=\s+['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, verstrline, re.M)
if mo:
    verstr = mo.group(1)
else:
    verstr = 'unknown'

setup(
    name='eobot-py',
    version=verstr,
    description='Eobot API wrapper',
    long_description='This module allows you to easily access the Eobot API',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: Freeware',
        'Programming Language :: Python :: 2.7',
        'Topic :: Utilities',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries'
    ],
    keywords='eobot eobot.com api',
    url='http://github.com/rickdenhaan/eobot-py',
    author='Rick den Haan',
    author_email='rick@capirussa.nl',
    license='Freeware',
    packages=['eobot'],
    include_package_data=True,
    install_requires=[
        'requests'
    ],
    zip_safe=False,
    test_suite='nose.collector',
    tests_require=['nose']
)
