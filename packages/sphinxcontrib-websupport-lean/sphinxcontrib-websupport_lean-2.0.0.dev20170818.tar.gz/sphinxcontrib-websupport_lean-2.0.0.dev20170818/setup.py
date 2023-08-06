# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages

long_desc = '''
sphinxcontrib-webuspport_lean provides a Python API to easily integrate Sphinx
documentation into your Web application.
'''

extras_require = {
    # Environment Marker works for wheel 0.24 or later
    'test': [
        'pytest',
        'mock',  # it would be better for 'test:python_version in 2.7'
    ],
}


def get_version():
    """Get version number of the package from version.py without importing core module."""
    package_dir = os.path.abspath(os.path.dirname(__file__))
    version_file = os.path.join(
        package_dir, 'sphinxcontrib/websupport_lean/version.py'
    )

    namespace = {}
    with open(version_file, 'rt') as f:
        exec(f.read(), namespace)

    return namespace['__version__']


setup(
    name='sphinxcontrib-websupport_lean',
    version=get_version(),
    url='https://devel.tech/site/open-source/',
    download_url='https://pypi.python.org/pypi/sphinxcontrib-websupport_lean',
    license='BSD',
    author='Georg Brandl',
    author_email='georg@python.org',
    description='Sphinx API for Web Apps',
    long_description=long_desc,
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Framework :: Sphinx',
        'Framework :: Sphinx :: Extension',
        'Topic :: Documentation',
        'Topic :: Documentation :: Sphinx',
        'Topic :: Text Processing',
        'Topic :: Utilities',
    ],
    platforms='any',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    extras_require=extras_require,
    namespace_packages=['sphinxcontrib'],
)
