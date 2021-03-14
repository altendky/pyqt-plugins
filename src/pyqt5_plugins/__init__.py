import os
import pathlib
import sys
import sysconfig

import PyQt5
import PyQt5.QtCore
import qt5_tools

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions

import pyqt5_plugins.utilities


pyqt_version = tuple(
    int(segment)
    for segment in PyQt5.QtCore.PYQT_VERSION_STR.split('.')
)

root = pathlib.Path(__file__).resolve().parent
# TODO: so apparently qml wants it all lower case...
if sys.platform == 'win32':
    root = pathlib.Path(pyqt5_plugins.utilities.fspath(root).lower())

if pyqt_version >= (5, 15, 4):
    qt_root = root.joinpath('Qt5')
else:
    qt_root = root.joinpath('Qt')

plugins = qt_root.joinpath('plugins')

pyqt5_root = pathlib.Path(PyQt5.__file__).resolve().parent
pyqt5_qml_path = qt_root.joinpath('qml')
pyqt5_plugins_path = qt_root.joinpath('plugins')


def create_environment(reference=None):
    if reference is None:
        reference = dict(os.environ)
    environment = qt5_tools.create_environment(reference=reference)

    if sys.platform == 'linux':
        environment.update(pyqt5_plugins.utilities.add_to_env_var_path_list(
            env=environment,
            name='LD_LIBRARY_PATH',
            before=[],
            after=[sysconfig.get_config_var('LIBDIR')],
        ))

    environment.update(pyqt5_plugins.utilities.add_to_env_var_path_list(
        env=environment,
        name='QT_PLUGIN_PATH',
        before=[],
        after=[
            pyqt5_plugins.utilities.fspath(pyqt5_plugins_path),
            pyqt5_plugins.utilities.fspath(plugins),
        ],
    ))
    # TODO: maybe also
    # PyQt5.QtCore.QLibraryInfo.location(
    #    PyQt5.QtCore.QLibraryInfo.PluginsPath,
    # )

    environment.update(pyqt5_plugins.utilities.add_to_env_var_path_list(
        env=environment,
        name='PYTHONPATH',
        before=sys.path,
        after=[''],
    ))
    environment.update(pyqt5_plugins.utilities.add_to_env_var_path_list(
        env=environment,
        name='PATH',
        before=sys.path,
        after=[''],
    ))

    return environment
