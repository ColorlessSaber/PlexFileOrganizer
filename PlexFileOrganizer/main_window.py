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

		# connect signals to slots
		self.view.start_create_list_of_media_files_signal.connect(self.model.create_list_of_media_files)
		self.model.create_list_of_media_files_complete_signal.connect(self.view.update_media_list_view)

		self.show()
