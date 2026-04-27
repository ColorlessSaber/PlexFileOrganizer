from PySide6 import (
    QtWidgets as qtw,
    QtCore as qtc,
)


class ApplicationPreferencesWindow(qtw.QDialog):

    def __init__(self, settings_data, parent=None):
        """
        Displays the settings available to the user that allow modification to the application, logging, etc.
        The settings are divided up into categories via tabs.

        :param settings_data: The settings data of the application
        :param parent: The parent window the dialog window will be linked to.
        """
        # The modal=True makes sure the user cannot click the main screen until they close the popup
        super().__init__(parent, modal=True)
        self.setWindowTitle("Preferences")
        self.setMinimumWidth(500)
        self.setMinimumHeight(300)

        self.__settings_data = settings_data

        # Logging settings tab
        self.cb_debug_logger_enable = qtw.QCheckBox("Enable Debug Logger", self)
        self.cb_debug_logger_enable.clicked.connect(self._toggle_apply_btn)
        self.cb_info_logger_enable = qtw.QCheckBox("Enable Info Logger", self)
        self.cb_info_logger_enable.clicked.connect(self._toggle_apply_btn)
        self.cb_warning_logger_enable = qtw.QCheckBox("Enable Warning Logger", self)
        self.cb_warning_logger_enable.clicked.connect(self._toggle_apply_btn)
        logging_settings_layout = qtw.QVBoxLayout()
        logging_settings_layout.addWidget(self.cb_debug_logger_enable)
        logging_settings_layout.addWidget(self.cb_info_logger_enable)
        logging_settings_layout.addWidget(self.cb_warning_logger_enable)
        groupbox_logger_options = qtw.QGroupBox("Logger Options", self)
        groupbox_logger_options.setLayout(logging_settings_layout)
        groupbox_logger_options.setFixedHeight(100)
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

        self.btn_clear_logs = qtw.QPushButton("Clear Logs", self)
        logging_buttons_layout = qtw.QHBoxLayout()
        logging_buttons_layout.addWidget(self.btn_clear_logs)

        main_logger_layout = qtw.QVBoxLayout()
        main_logger_layout.addWidget(groupbox_logger_options)
        main_logger_layout.addLayout(logging_buttons_layout)

        container_for_logging_tab = qtw.QWidget()
        container_for_logging_tab.setLayout(main_logger_layout)

        # Create tabs
        tab_widget = qtw.QTabWidget()
        tab_widget.addTab(container_for_logging_tab, "Logging")

        self._setup_preferences_per_setting_data()

        # set up the layout of window
        self.btn_cancel = qtw.QPushButton("Cancel", self)
        self.btn_cancel.clicked.connect(self.reject)
        self.btn_apply = qtw.QPushButton("Apply", self)
        self.btn_apply.clicked.connect(self.apply_changes_save_and_close)
        self.btn_apply.setProperty("btnName", "apply")
        self.btn_apply.setEnabled(False)
        self.btn_ok = qtw.QPushButton("OK", self)
        self.btn_ok.clicked.connect(self.apply_changes_save_and_close)
        self.btn_ok.setProperty("btnName", "ok")
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

    def _setup_preferences_per_setting_data(self) -> None:
        """
        Setup the preferences per application settings data/json file.

        :return: None
        """

        self.cb_info_logger_enable.setChecked(
            self.__settings_data.get("logging_settings").get("enable_info_logs")
        )
        self.cb_debug_logger_enable.setChecked(
            self.__settings_data.get("logging_settings").get("enable_debug_logs")
        )
        self.cb_warning_logger_enable.setChecked(
            self.__settings_data.get("logging_settings").get("enable_warning_logs")
        )

    def _toggle_apply_btn(self) -> None:
        """
        Toggle the apply button state.
        """
        # Run though all the tabs and check to see if any settings are different compared to the __settings_data
        # if so, enable the apply button

        there_are_changes = False
        ## Check logging tab
        if self.cb_debug_logger_enable.isChecked() != self.__settings_data.get("logging_settings").get('enable_debug_logs'):
            there_are_changes = True

        if self.cb_info_logger_enable.isChecked() != self.__settings_data.get("logging_settings").get('enable_info_logs'):
            there_are_changes = True

        if self.cb_warning_logger_enable.isChecked() != self.__settings_data.get("logging_settings").get('enable_warning_logs'):
            there_are_changes = True

        if there_are_changes:
            self.btn_apply.setEnabled(True)
        else:
            self.btn_apply.setEnabled(False)

    def apply_changes_save_and_close(self):
        """
        Apply the changes in settings, save the changes, and then close the window.
        """
        button_pressed = self.sender()

        # Run through all the tabs and check to see what settings are different compared to the __settings_data
        # Apply any differences between the two

        # save the new settings configuration

        if button_pressed.property("btnName") == "ok": # only close the window if the btn_ok was pressed
            self.accept()
