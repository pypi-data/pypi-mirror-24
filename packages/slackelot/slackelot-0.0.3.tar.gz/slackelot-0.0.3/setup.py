import setuptools
from setuptools import  setup, find_packages

from io import open
from os import path

try:
    from pypandoc import convert

    def read_md(f):
        return convert(f, 'rst')
except ImportError:
    print("warning: pypandoc module not found, could not convert Markdown to RST")

    def read_md(f):
        return open(f, 'r', encoding='utf-8').read()


INSTALL_REQUIRES = ['requests', 'pytest', 'pypandoc']
EXTRAS_REQUIRE = {}

PACKAGES = find_packages(exclude=['contrib', 'docs', 'tests'])

CLASSIFIERS = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Natural Language :: English',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Topic :: Software Development :: Libraries :: Python Modules',
]

# Thanks to Hynek Schlawack for explaining conditional python dependencies
# https://hynek.me/articles/conditional-python-dependencies/
if int(setuptools.__version__.split(".", 1)[0]) < 18:
    assert "bdist_wheel" not in sys.argv, "setuptools 18 required for wheels."
    # For legacy setuptools + sdist.
    if sys.version_info[0:2] < (3, 3):
        INSTALL_REQUIRES.append('mock')
else:
    EXTRAS_REQUIRE[":python_version<'3.3'"] = ['mock']


if __name__ == '__main__':
    setup(
        name='slackelot',
        version='0.0.3',
        description='A simple wrapper around the Slack web api to post messages',
        long_description=read_md('README.md'),
        url='https://github.com/Chris-Graffagnino/slackelot',
        author='Chris Graffagnino',
        author_email='graffwebdev@gmail.com',
        license='MIT',
        keywords='slack',
        python_requires='>=2.7',
        classifiers=CLASSIFIERS,
        install_requires=INSTALL_REQUIRES,
        extras_require=EXTRAS_REQUIRE,
        packages=PACKAGES,
    )
