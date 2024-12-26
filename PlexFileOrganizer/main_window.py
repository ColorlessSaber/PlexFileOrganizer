"""
The main window for the application
"""
from PySide6 import QtWidgets as qtw
from PySide6 import QtCore as qtc
from PySide6 import QtGui as qtg
from PlexFileOrganizer.model import Model
from PlexFileOrganizer.view import View


class MainWindow(qtw.QMainWindow):

	def __init__(self):
		super().__init__()

		self.view = View()
		self.model = Model()
		self.setCentralWidget(self.view)

		self.statusBar().addPermanentWidget(qtw.QLabel('Version 2.0.0'))

		# connect signals to slots
		self.view.start_creating_media_folders_signal.connect(self.model.create_media_folders_thread)

		self.show()
