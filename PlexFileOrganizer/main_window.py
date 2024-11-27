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
		self.view.start_analyzing_media_folder_signal.connect(self.model.analyze_media_folder)
		self.view.start_update_file_names_thread_signal.connect(self.model.update_file_names)

		self.model.analyzation_of_media_folder_complete_signal.connect(self.view.update_media_information_view)
		self.model.error_message_signal.connect(self.view.error_message_popup)
		self.model.update_file_names_complete_signal.connect(self.view.completed_message_popup)

		self.show()
