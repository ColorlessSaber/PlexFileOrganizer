from PySide6 import (
    QtWidgets as qtw,
    QtCore as qtc,
    QtGui as qtg,
)


class ApplicationPreferencesWindow(qtw.QDialog):

    def __init__(self, parent=None):
        """
        Displays the settings available to the user that allow modification to the application, logging, etc.
        The settings are divided up into categories via tabs.

        :param parent: The parent window the dialog window will be linked to.
        """
        # The modal=True makes sure the user cannot click the main screen until they close the popup
        super().__init__(parent, modal=True)
        self.setWindowTitle("Preferences")
        self.setFixedWidth(500)
        self.setFixedHeight(500)

        # Logging settings tab
        self.cb_debug_logger_enable = qtw.QCheckBox("Enable Debug Logger", self)
        self.cb_info_logger_enable = qtw.QCheckBox("Enable Info Logger", self)
        logging_settings_layout = qtw.QVBoxLayout()
        logging_settings_layout.addWidget(self.cb_debug_logger_enable)
        logging_settings_layout.addWidget(self.cb_info_logger_enable)
        groupbox_logger_options = qtw.QGroupBox("Logger Options", self)
        groupbox_logger_options.setLayout(logging_settings_layout)
        groupbox_logger_options.setStyleSheet(
            """
            QGroupBox {
                border: 2px solid grey;
                border-radius: 5px;
                padding-top: 16px;
                font-weight: bold;
            }
            """
        )

        main_logger_layout = qtw.QVBoxLayout()
        main_logger_layout.addWidget(groupbox_logger_options)

        container_for_logging_tab = qtw.QWidget()
        container_for_logging_tab.setLayout(main_logger_layout)

        # Create tabs
        tab_widget = qtw.QTabWidget()
        tab_widget.addTab(container_for_logging_tab, "Logging")


        # set up the layout of window
        self.btn_cancel = qtw.QPushButton("Cancel", self)
        self.btn_cancel.clicked.connect(self.reject)
        self.btn_apply = qtw.QPushButton("Apply", self)
        self.btn_ok = qtw.QPushButton("OK", self)
        self.btn_ok.setDefault(True)
        self.btn_ok.setAutoDefault(True)
        window_buttons_layout = qtw.QHBoxLayout()
        window_buttons_layout.addWidget(self.btn_cancel)
        window_buttons_layout.addWidget(self.btn_apply)
        window_buttons_layout.addWidget(self.btn_ok)
        window_buttons_layout.setAlignment(qtc.Qt.AlignmentFlag.AlignRight)

        main_layout = qtw.QVBoxLayout()
        main_layout.addWidget(tab_widget)
        main_layout.addLayout(window_buttons_layout)
        self.setLayout(main_layout)
