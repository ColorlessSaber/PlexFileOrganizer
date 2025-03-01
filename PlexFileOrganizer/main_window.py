from PySide6 import QtWidgets as qtw
from PySide6 import QtCore as qtc
from PySide6 import QtGui as qtg

from PlexFileOrganizer.model import Model
from PlexFileOrganizer.view import View


class MainWindow(qtw.QMainWindow):
	"""The main window for the application"""

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
		self.view.initiate_creating_media_folder_signal.connect(self.model.start_create_media_folder_thread)
		self.view.user_input_response_signal.connect(self.model.user_input_response_signal)
		self.view.initiate_scan_of_directory_signal.connect(self.model.start_scan_of_directory_thread)

		self.model.user_input_request_signal.connect(self.view.launch_user_input_request_popup)
		self.model.update_progress_signal.connect(self.update_progress_bar_and_print_message)

		self.show()

	def update_progress_bar_and_print_message(self, progress_bar_percentage, status_message):
		"""
		Update the progress bar and print message on Log Window

		:param progress_bar_percentage: The int value for the progress bar
		:param status_message: Message to display on the status bar
		:return:
		"""
		self.progress_bar.setValue(progress_bar_percentage)
		self.view.write_to_log_window(status_message)
