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

		self.progress_bar = qtw.QProgressBar()
		self.progress_bar.setMinimum(0)
		self.progress_bar.setMaximum(100)
		self.statusBar().addPermanentWidget(self.progress_bar)

		self.statusBar().addPermanentWidget(qtw.QLabel('Version 2.0.0'))

		# connect signals to slots
		self.view.start_creating_media_folders_signal.connect(self.model.start_create_media_folders_thread)

		self.show()

	def update_progress_bar(self, value):
		"""
		Update the progress bar.

		:param value: the percentage progress bar should be at.
		:return:
		"""
		self.progress_bar.setValue(value)
