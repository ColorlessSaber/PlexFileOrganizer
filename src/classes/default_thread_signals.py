from PySide6 import QtCore as qtc


class DefaultThreadSignals(qtc.QObject):
    """
    Default thread signals

    error -- Signal to indicate an error has occurred
    progress -- Signal to update the progress bar and display a message
    finished -- Signal to indicate the thread is finished. Can be overwritten to output an object or a specific datatype
    """

    error = qtc.Signal()
    progress = qtc.Signal(int, str)
    finished = qtc.Signal()
