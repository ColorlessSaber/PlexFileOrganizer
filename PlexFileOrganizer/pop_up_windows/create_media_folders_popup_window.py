"""
Pop-up window to allow user to create folder(s) per media type-TV show or movie
"""
from PySide6 import QtWidgets as qtw
from PySide6 import QtCore as qtc

class CreateMediaFolders(qtw.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlag(qtc.Qt.WindowStaysOnTopHint)

        # widgets
        self.media_type_group = qtw.QGroupBox('Media Type')
        self.media_type_movie_selected = qtw.QRadioButton('Movie', self)
        self.media_type_tv_selected = qtw.QRadioButton('TV Show', self)
        self.media_type_group.setLayout(qtw.QHBoxLayout())
        self.media_type_group.layout().addWidget(self.media_type_movie_selected)
        self.media_type_group.layout().addWidget(self.media_type_tv_selected)

        self.media_inform_form = qtw.QFormLayout()
        self.media_title = qtw.QLineEdit(self)
        self.season_number = qtw.QLineEdit(self)
        self.media_inform_form.addRow('Title:', self.media_title)
        self.media_inform_form.addRow('Season #:', self.season_number)

        # layout
        main_layout = qtw.QVBoxLayout()
        main_layout.addWidget(self.media_type_group)
        main_layout.addLayout(self.media_inform_form)
