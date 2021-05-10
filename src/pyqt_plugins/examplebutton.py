from . import import_it

QtWidgets = import_it("PyQt", "QtWidgets")


class ExampleButton(QtWidgets.QPushButton):
    def __init__(self, parent):
        super().__init__(parent)

        self.setText('pyqt5-tools Example Button')
