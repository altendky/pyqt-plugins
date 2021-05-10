import sys
sys.stderr.write('exampleqmlitemplugin.py debug: : just imported sys\n')
sys.stderr.flush()
import traceback
sys.stderr.write('exampleqmlitemplugin.py debug: : just imported traceback\n')
sys.stderr.flush()

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


QtQml = import_it("PyQt", "QtQml")
sys.stderr.write('exampleqmlitemplugin.py debug: : just imported QtQml\n')
sys.stderr.flush()

pyqt_plugins = import_it("pyqt_plugins")
import_it("pyqt_plugins", "examples", "exampleqmlitem")
sys.stderr.write('exampleqmlitemplugin.py debug: : just imported pyqt5_plugins.examples.exampleqmlitem\n')
sys.stderr.flush()


class ExampleQmlItemPlugin(QtQml.QQmlExtensionPlugin):
    def registerTypes(self, uri):
        sys.stderr.write('exampleqmlitemplugin.py debug: ExampleQmlItemPlugin.registerTypes(): uri - {!r}\n'.format(uri))
        sys.stderr.flush()
        try:
            QtQml.qmlRegisterType(
                pyqt_plugins.examples.exampleqmlitem.ExampleQmlItem,
                'examples',
                1,
                0,
                'ExampleQmlItem',
            )
        except Exception as e:
            sys.stderr.write('exampleqmlitemplugin.py debug: ExampleQmlItemPlugin.registerTypes(): exception - {!r}\n'.format(e))
            sys.stderr.flush()
            traceback.print_exc(file=sys.stderr)
            sys.stderr.flush()
            raise

        sys.stderr.write('exampleqmlitemplugin.py debug: ExampleQmlItemPlugin.registerTypes(): about to return None\n')
        sys.stderr.flush()
        return None


sys.stderr.write('exampleqmlitemplugin.py debug: : import complete\n')
sys.stderr.flush()
