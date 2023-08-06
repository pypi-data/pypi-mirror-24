import os
import sys

from setuptools import find_packages, setup

try:
    import pypandoc
    long_description = pypandoc.convert_file('README.md', 'rst')
except (OSError, IOError, ImportError):
    long_description = open('README.md').read()


def setup_package():
    src_path = os.path.dirname(os.path.abspath(sys.argv[0]))
    old_path = os.getcwd()
    os.chdir(src_path)
    sys.path.insert(0, src_path)

    needs_pytest = {'pytest', 'test', 'ptr'}.intersection(sys.argv)
    pytest_runner = ['pytest-runner'] if needs_pytest else []

    setup_requires = pytest_runner
    install_requires = []
    tests_require = ['pytest']

    metadata = dict(
        name='brent-search',
        version='1.0.19',
        maintainer="Danilo Horta",
        maintainer_email="horta@ebi.ac.uk",
        description="Brent's method for univariate function optimization.",
        long_description=long_description,
        license="MIT",
        url='http://github.com/limix/brent-search',
        packages=find_packages(),
        zip_safe=True,
        include_package_data=True,
        install_requires=install_requires,
        setup_requires=setup_requires,
        tests_require=tests_require,
        classifiers=[
            "Development Status :: 5 - Production/Stable",
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python :: 2.7",
            "Programming Language :: Python :: 3.5",
            "Programming Language :: Python :: 3.6",
            "Operating System :: OS Independent",
        ], )

    try:
        setup(**metadata)
    finally:
        del sys.path[0]
        os.chdir(old_path)


if __name__ == '__main__':
    setup_package()
