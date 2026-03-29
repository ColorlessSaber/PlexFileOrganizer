## _Coming Up Versions_
### _Version 3_
**Features**
- [ ] Organize the media folder--AKA, the music folder.

### _Version 2_
**Features**
- [ ] Use an SQLite database to quickly add/remove folders and content to existing media folders.

### _Version 1.2_
**Features**
- [ ] Built in media player to allow user to watch to see which episode the media file is.
- [ ] Update subtitle file(s) to have the same name as updated file that are associated with.

## _Next Version in the Works_
N/A

## _Current Version_
### _Version 1.1.2_
**Bug Fixes**
- Manual media file update would identify the wrong file to update.

**Performance**
- Under-the-hood optimization.

### _Version 1.1.1_
**Bug Fixes**
- Fixed issue for modified media folder not working when its a movie media folder

**Misc.**
- Added more process messages when doing auto update media files

## _Previous Versions_
### _Version 1.1_
**Features**
- [x] Create a Special season folder for TV show.
<br><br>
**Performance**
- Optimized code for better performance.
<br><br>
**Misc.**
- Added styling to the windows.


### _Version 1.0.1_
**Bug Fixes**
- Typo of method name in create_media_folder_thread.py.
- typo of method name in update_existing_media_folder_thread.py.

### _Version 1_
**Features**
- [x] Create a media folder for a new movie or TV show, along with sub-folders for miscellaneous content--trailers, extra, etc.
- [X] Add a new season folder and or extra folder to an existing TV show media folder.
- [X] Automatically go through the selected folder and identify the media files that need to be updated and rename the file accordingly.
  - [X] know what episode number to start from for new media files if there are existing ones already in the folder.
- [X] Allow the user to manually rename media files--new or existing--in an existing folder.
