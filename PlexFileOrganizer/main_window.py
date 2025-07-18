from PySide6 import QtWidgets as qtw
from PySide6 import QtCore as qtc

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

		self.statusBar().addPermanentWidget(qtw.QLabel('Version 0.5.0'))

		# view signals to be connected to model slots
		self.view.signal_initiate_creating_media_folder.connect(self.model.start_create_media_folder_thread)
		self.view.signal_user_confirmation_of_existing_media_folder.connect(self.model.signal_user_confirmation_of_existing_media_folder)
		self.view.signal_initiate_auto_update_media_files.connect(self.model.start_auto_update_media_files_thread)

		# view signals to be connected to main_window slots
		self.view.signal_reset_progress_bar.connect(self.slot_reset_progress_bar)

		# model signals to be connected to view slots
		self.model.signal_inform_user_of_existing_media_folder.connect(self.view.messagebox_inform_user_of_existing_media_file)
		self.model.signal_update_progress.connect(self.slot_update_progress_bar_and_print_message)

		# model signals to be connected to main_window slots
		self.model.signal_finished.connect(self.slot_finished_task)
		self.model.signal_error_message.connect(self.slot_display_error_message)

		self.show()

# *** Slots for model/view inputs***
	@qtc.Slot(int, str)
	def slot_update_progress_bar_and_print_message(self, progress_bar_percentage, status_message):
		"""
		Update the progress bar and print message on Log Window

		:param progress_bar_percentage: The int value for the progress bar
		:param status_message: Message to display on the status bar
		:return:
		"""
		self.progress_bar.setValue(progress_bar_percentage)
		self.view.write_to_log_window(status_message)

	@qtc.Slot(object)
	def slot_display_error_message(self, error_message):
		"""
		Write the error message to the Log Window and reset the progress bar.

		:param error_message: The error that was generated
		:return:
		"""
		self.progress_bar.reset()
		self.view.write_to_log_window('\n!!Error has been detected!! -> {}'.format(repr(error_message)))

	@qtc.Slot(str)
	def slot_finished_task(self, the_task_completed):
		"""
		Makes the View launch the correct messagebox to inform the user the task is completed

		:param the_task_completed:
		:return:
		"""
		if the_task_completed == 'auto_update':
			self.view.messagebox_auto_update_media_files_complete()
		else:
			pass

	def slot_reset_progress_bar(self):
		"""
		Reset the progress bar

		:return:
		"""
		self.progress_bar.reset()
