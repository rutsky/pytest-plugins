# Common setup.py code shared between all the projects in this repository
import sys
import logging

from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    pytest_args = []
    src_dir = None

    def initialize_options(self):
        TestCommand.initialize_options(self)

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        global pytest_args
        logging.basicConfig(format='%(asctime)s %(levelname)s %(name)s %(message)s', level='DEBUG')

        # import here, cause outside the eggs aren't loaded
        import pytest

        self.pytest_args.extend(['--cov', self.src_dir,
                     '--cov-report', 'xml',
                     '--cov-report', 'html',
                     '--junitxml', 'junit.xml',
                     ])
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


def common_setup(src_dir):
    readme_file = 'README.md'
    changelog_file = 'CHANGES.md'
    version_file = 'VERSION'

    # Convert Markdown to RST for PyPI
    try:
        import pypandoc
        long_description = pypandoc.convert(readme_file, 'rst')
        changelog = pypandoc.convert(changelog_file, 'rst')
    except (IOError, ImportError, OSError):
        long_description = open(readme_file).read()
        changelog = open(changelog_file).read()

    # Gather trailing arguments for pytest, this can't be done using setuptools' api
    if 'test' in sys.argv:
        PyTest.pytest_args = sys.argv[sys.argv.index('test') + 1:]
        if PyTest.pytest_args:
            sys.argv = sys.argv[:-len(PyTest.pytest_args)]
    PyTest.src_dir = src_dir

    return dict(
            # Version is shared between all the projects in this repo
            version=open(version_file).read().strip(),
            long_description='\n'.join((long_description, changelog)),
            url='https://github.com/manahl/pytest-plugins',
            license='MIT license',
            platforms=['unix', 'linux'],
            cmdclass={'test': PyTest},
            setup_requires=['setuptools-git'],
            include_package_data=True
            )
