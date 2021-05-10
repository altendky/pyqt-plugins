import os
import pathlib
import subprocess
import time

import pytest

# TODO: CAMPid 0970432108721340872130742130870874321
import importlib
import pkg_resources

major = int(pkg_resources.get_distribution(__name__.partition('.')[0]).version.partition(".")[0])


def import_it(*segments):
    m = {
        "pyqt_tools": "pyqt{major}_tools".format(major=major),
        "pyqt_plugins": "pyqt{major}_plugins".format(major=major),
        "qt_tools": "qt{major}_tools".format(major=major),
        "qt_applications": "qt{major}_applications".format(major=major),
        "PyQt": "PyQt{major}".format(major=major),
    }

    majored = [m[segments[0]], *segments[1:]]
    return importlib.import_module(".".join(majored))


qt_tools = import_it("qt_tools")
pyqt_plugins = import_it("pyqt_plugins")
import_it("pyqt_plugins", "examples", "exampleqmlitem")
import_it("pyqt_plugins", "tests", "testbutton")
import_it("pyqt_plugins", "tests", "testbuttonplugin")
import_it("pyqt_plugins", "utilities")


fspath = getattr(os, 'fspath', str)


vars_to_print = [
    *pyqt_plugins.utilities.diagnostic_variables_to_print,
    pyqt_plugins.examples.exampleqmlitem.test_path_env_var,
    pyqt_plugins.tests.testbutton.test_path_env_var,
]


@pytest.fixture(name='environment')
def environment_fixture():
    environment = pyqt_plugins.create_environment(os.environ)
    pyqt_plugins.utilities.mutate_qml_path(environment, paths=qml2_import_paths)
    environment['QT_DEBUG_PLUGINS'] = '1'

    return environment


def run_for_file(
        *args,
        file_path,
        file_exists_timeout=60,
        file_write_time_allowance=5,
        **kwargs
):
    process = subprocess.Popen(*args, **kwargs)

    deadline = time.monotonic() + file_exists_timeout

    while True:
        time.sleep(1)

        if process.poll() is not None:
            raise Exception('process ended')

        if file_path.exists():
            break

        if time.monotonic() > deadline:
            raise Exception(
                'file not written with {} seconds'.format(file_exists_timeout),
            )

    time.sleep(file_write_time_allowance)

    return file_path.read_bytes()


def test_designer_creates_test_widget(tmp_path, environment):
    file_path = tmp_path/'tigger'
    environment[pyqt_plugins.tests.testbutton.test_path_env_var] = fspath(file_path)

    widget_plugin_path = pathlib.Path(
        pyqt_plugins.tests.testbuttonplugin.__file__,
    ).parent

    environment.update(pyqt_plugins.utilities.add_to_env_var_path_list(
        env=environment,
        name='PYQTDESIGNERPATH',
        before=[fspath(widget_plugin_path)],
        after=[''],
    ))

    pyqt_plugins.utilities.print_environment_variables(environment, *vars_to_print)

    contents = run_for_file(
        [fspath(qt_tools.application_path('designer'))],
        env=environment,
        file_path=file_path,
    )

    assert contents == pyqt_plugins.tests.testbutton.test_file_contents


qml2_import_paths = (pyqt_plugins.utilities.fspath(pyqt_plugins.root),)


def test_qmlscene_paints_test_item(tmp_path, environment):
    file_path = tmp_path/'eeyore'
    environment[pyqt_plugins.examples.exampleqmlitem.test_path_env_var] = fspath(file_path)

    qml_example_path = pyqt_plugins.utilities.fspath(
        pathlib.Path(pyqt_plugins.examples.__file__).parent / 'qmlapp.qml'
    )

    pyqt_plugins.utilities.print_environment_variables(environment, *vars_to_print)

    contents = run_for_file(
        [
            fspath(qt_tools.application_path('qmlscene')),
            fspath(qml_example_path),
        ],
        env=environment,
        file_path=file_path,
    )

    assert contents == pyqt_plugins.examples.exampleqmlitem.test_file_contents


def test_qmltestrunner_paints_test_item(tmp_path, environment):
    file_path = tmp_path/'piglet'
    environment[pyqt_plugins.examples.exampleqmlitem.test_path_env_var] = fspath(file_path)

    qml_test_path = pyqt_plugins.utilities.fspath(
        pathlib.Path(pyqt_plugins.examples.__file__).parent / 'qmltest.qml'
    )

    pyqt_plugins.utilities.print_environment_variables(environment, *vars_to_print)

    subprocess.run(
        [
            fspath(qt_tools.application_path('qmltestrunner')),
            '-input',
            qml_test_path,
        ],
        check=True,
        env=environment,
        timeout=60,
    )

    assert (
            file_path.read_bytes()
            == pyqt_plugins.examples.exampleqmlitem.test_file_contents
    )
