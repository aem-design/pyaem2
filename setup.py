from __future__ import print_function
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import sys

class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ['--strict', '--verbose', '--tb=long', 'test']
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)

setup(
    name='pyaem2',
    version='2.0.1',
    url='http://github.com/aem-design/pyaem2/',
    license='Apache 2.0',
    author='Max Barrass',
    tests_require=['mock', 'pytest'],
    install_requires=['BeautifulSoup4>=4.6.0', 'pycurl>=7.43.0', 'xmltodict>=0.10.2'],
    cmdclass={'test': PyTest},
    author_email='max.barrass@gmail.com',
    description='Python client for Adobe Experience Manager (AEM) API',
    long_description='Python client for Adobe Experience Manager (AEM) API',
    packages=['pyaem2'],
    include_package_data=True,
    platforms='any',
    test_suite='pyaem2.test.test_pyaem2',
    classifiers = [
        'Programming Language :: Python',
        'Development Status :: 5 - Production/Stable',
        'Natural Language :: English',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        ],
    extras_require={
        'testing': ['pytest'],
    }
)
