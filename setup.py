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
    name='pyaem',
    version='0.9.1',
    url='http://github.com/cliffano/pyaem/',
    license='MIT License',
    author='Cliffano Subagio',
    tests_require=['mock', 'pytest'],
    install_requires=['BeautifulSoup>=3.2.1',
                    'pycurl>=7.19.0.0'
                    ],
    cmdclass={'test': PyTest},
    author_email='cliffano@gmail.com',
    description='Python client for Adobe Experience Manager (AEM) API',
    long_description='Python client for Adobe Experience Manager (AEM) API',
    packages=['pyaem'],
    include_package_data=True,
    platforms='any',
    test_suite='pyaem.test.test_pyaem',
    classifiers = [
        'Programming Language :: Python',
        'Development Status :: 4 - Beta',
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
