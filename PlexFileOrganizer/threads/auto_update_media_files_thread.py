"""
Thread for Auto Update Media Files
"""
import pathlib
from PySide6 import QtCore as qtc
from PlexFileOrganizer.functions import (directory_scanner,
                                         FolderAndFilePatterns,
                                         automatic_media_file_update,
                                         find_media_files_in_dir,
                                         video_file_condition)

class ThreadSignals(qtc.QObject):
    """
    The signals for the thread
    """
    error = qtc.Signal(object)
    finished = qtc.Signal(str)
    progress = qtc.Signal(int, str)

class AutoUpdateMediaFilesThread(qtc.QRunnable):

    def __init__(self, directory_and_options):
        """

        :param directory_and_options: The directory that contains the directory user selected, and other selectable options.
        """
        super().__init__()
        self.directory_and_options = directory_and_options
        self.signals = ThreadSignals()

    @qtc.Slot()
    def run(self):
        """
        Initialize the thread

        :return:
        """
        folder_and_file_pattern = FolderAndFilePatterns()

        # will hold all media file(s) that are in the same directory.
        # primary use is for tv show season folders, allowing for easier naming of the files.
        media_files_in_same_dir = []

        try:
            self.signals.progress.emit(50, 'Scanning directory...')
            # with each list of files in a directory, check to see if any of them are not formated correctly.
            for file_list in find_media_files_in_dir(video_file_condition, self.directory_and_options['directory']):
                all_files_are_formatted_correctly = folder_and_file_pattern.check_files_in_folder(file_list)
                if not all_files_are_formatted_correctly:
                    print(file_list)
                else:
                    continue

            # print('finished the check') # for debugging
            self.signals.progress.emit(100, 'Finished scanning.')
            self.signals.finished.emit('auto_update')

            """ OLD CODE BELOW
            for entry in directory_scanner(self.directory_and_options['directory']):
                if any(entry.path.endswith(file_extension) for file_extension in ['.mkv', '.mp4', '.avi']):
                    # Skip checking the media files in Extra Folders, unless the option in directory_and_options
                    # says we need to check them.
                    # When the 'scan_extra_folder' folder is set to false, the media file in the Extra folder is skipped -- I.E.,
                    # its assumed the file is formated correctly.
                    if folder_and_file_pattern.extra_folder_check(entry.path) and not self.directory_and_options['scan_extra_folder']:
                        continue

                    # Compare the new media file to the last appended file in the list to see if they are in
                    # the same directory. If they are, append the media file to the list.
                    if len(media_files_in_same_dir) > 0:
                        last_appended_file = media_files_in_same_dir[-1]
                        if pathlib.Path(last_appended_file).parent.resolve() == pathlib.Path(entry.path).parent.resolve():
                            media_files_in_same_dir.append(entry)
                        else:

                            # loop through the media files in the list, checking to see if any of them are not formated
                            # correctly fo the folder it is in.
                            all_files_are_formatted_incorrectly = check_files_in_media_folder(media_files_in_same_dir)
                            if not all_files_are_formatted_incorrectly:
                                message_to_user = automatic_media_file_update(media_files_in_same_dir)
                                if message_to_user: # if the string has something, send it off
                                    self.signals.progress.emit(50, message_to_user)
                            media_files_in_same_dir = [entry]  # clear the list and append the lastest media file for new group folder check

                    else:
                        media_files_in_same_dir.append(entry)

            # The case when the user selects a media folder or a sub-media folder versus a folder containing several media folder(s).
            all_files_are_formatted_incorrectly = check_files_in_media_folder(media_files_in_same_dir)
            if not all_files_are_formatted_incorrectly:
                message_to_user = automatic_media_file_update(media_files_in_same_dir)
                if message_to_user:  # if the string has something, send it off
                    self.signals.progress.emit(50, message_to_user)
            """
        finally:
            print('hello')
        """ COMMENTED OUT FOR JUST FOR DEBUGGING
        except OSError as e:
            self.signals.error.emit(e)

        except BaseException as e:
            # bad use of an exception, but required to catch an error for something that isn't covered for.
            self.signals.error.emit(e)
        """