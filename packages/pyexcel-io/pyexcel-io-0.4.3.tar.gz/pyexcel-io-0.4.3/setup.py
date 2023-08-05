try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages
import sys
PY2 = sys.version_info[0] == 2
PY26 = PY2 and sys.version_info[1] < 7

NAME = 'pyexcel-io'
AUTHOR = 'C.W.'
VERSION = '0.4.3'
EMAIL = 'wangc_2011@hotmail.com'
LICENSE = 'New BSD'
DESCRIPTION = (
    'A python library to read and write structured data in csv, zipped csv ' +
    'format and to/from databases' +
    ''
)
URL = 'https://github.com/pyexcel/pyexcel-io'
DOWNLOAD_URL = '%s/archive/0.4.3.tar.gz' % URL
FILES = ['README.rst', 'CHANGELOG.rst']
KEYWORDS = [
    'API',
    'tsv',
    'tsvz'
    'csv',
    'csvz'
    'python'
]

CLASSIFIERS = [
    'Topic :: Office/Business',
    'Topic :: Utilities',
    'Topic :: Software Development :: Libraries',
    'Programming Language :: Python',
    'License :: OSI Approved :: BSD License',
    'Intended Audience :: Developers',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: Implementation :: PyPy'
]

INSTALL_REQUIRES = [
    'lml==0.0.1',
]

if PY26:
    INSTALL_REQUIRES.append('ordereddict')

PACKAGES = find_packages(exclude=['ez_setup', 'examples', 'tests'])
EXTRAS_REQUIRE = {
    'xls': ['pyexcel-xls>=0.4.0'],
    'xlsx': ['pyexcel-xlsx>=0.4.0'],
    'ods': ['pyexcel-ods3>=0.4.0'],
}


def read_files(*files):
    """Read files into setup"""
    text = ""
    for single_file in files:
        content = read(single_file)
        text = text + content + "\n"
    return text


def read(afile):
    """Read a file into setup"""
    with open(afile, 'r') as opened_file:
        content = filter_out_test_code(opened_file)
        content = "".join(list(content))
        return content


def filter_out_test_code(file_handle):
    found_test_code = False
    for line in file_handle.readlines():
        if line.startswith('.. testcode:'):
            found_test_code = True
            continue
        if found_test_code is True:
            if line.startswith('  '):
                continue
            else:
                empty_line = line.strip()
                if len(empty_line) == 0:
                    continue
                else:
                    found_test_code = False
                    yield line
        else:
            for keyword in ['|version|', '|today|']:
                if keyword in line:
                    break
            else:
                yield line


if __name__ == '__main__':
    setup(
        name=NAME,
        author=AUTHOR,
        version=VERSION,
        author_email=EMAIL,
        description=DESCRIPTION,
        url=URL,
        download_url=DOWNLOAD_URL,
        long_description=read_files(*FILES),
        license=LICENSE,
        keywords=KEYWORDS,
        extras_require=EXTRAS_REQUIRE,
        tests_require=['nose'],
        install_requires=INSTALL_REQUIRES,
        packages=PACKAGES,
        include_package_data=True,
        zip_safe=False,
        classifiers=CLASSIFIERS
    )
