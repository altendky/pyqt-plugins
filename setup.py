import os
import pathlib

import setuptools
import versioneer

import build


fspath = getattr(os, 'fspath', str)


here = pathlib.Path(__file__).parent


class InvalidVersionError(Exception):
    pass


def pad_version(v, segment_count=3):
    split = v.split('.')

    if len(split) > segment_count:
        raise InvalidVersionError('{} has more than three segments'.format(v))

    return '.'.join(split + ['0'] * (segment_count - len(split)))


# TODO: really doesn't seem quite proper here and probably should come
#       in some other way?
pyqt_version = pad_version(os.environ.setdefault('PYQT_VERSION', '5.15.1'))
qt_version = pad_version(os.environ.setdefault('QT_VERSION', '5.15.1'))
qt_major_version = qt_version.partition('.')[0]

pyqt5_plugins_wrapper_version = versioneer.get_versions()['version']
pyqt5_plugins_version = '{}.{}'.format(
    pyqt_version,
    pyqt5_plugins_wrapper_version,
)

# When using ~=, don't pad because that affects allowed versions.  The last
# segment is the one that is allowed to increase.
qt_tools_wrapper_version = '1.0'

# Must be False for release.  PyPI won't let you uplaod with a URL dependency.
use_qt_tools_url = True

if use_qt_tools_url:
    qt_tools_url = ' @ git+https://github.com/altendky/qt-tools@main'
    qt_tools_version_specifier = ''
else:
    qt_tools_url = ''
    qt_tools_version_specifier = '~={}.{}.dev0'.format(
        qt_version,
        qt_tools_wrapper_version,
    )


with open('README.rst') as f:
    readme = f.read()


class Dist(setuptools.Distribution):
    def has_ext_modules(self):
        # Event if we don't have extension modules (e.g. on PyPy) we want to
        # claim that we do so that wheels get properly tagged as Python
        # specific.  (thanks dstufft!)
        return True


setuptools.setup(
    name="pyqt5_plugins",
    description="PyQt Designer and QML plugins",
    long_description=readme,
    long_description_content_type='text/x-rst',
    url='https://github.com/altendky/pyqt5-tools',
    author="Kyle Altendorf",
    author_email='sda@fstab.net',
    license='GPLv3',
    classifiers=[
        # complete classifier list: https://pypi.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 4 - Beta',
        'Environment :: Win32 (MS Windows)',
        'Environment :: X11 Applications :: Qt',
        'Intended Audience :: Developers',
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development',
        'Topic :: Utilities',
    ],
    cmdclass={'build_py': build.BuildPy},
    distclass=Dist,
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},
    version=pyqt5_plugins_version,
    include_package_data=True,
    python_requires=">=3.5",
    install_requires=[
        'click',
        'pyqt5=={}'.format(os.environ['PYQT_VERSION']),
        'qt{}-tools{}{}'.format(
            qt_major_version,
            qt_tools_version_specifier,
            qt_tools_url,
        ),
    ],
)
