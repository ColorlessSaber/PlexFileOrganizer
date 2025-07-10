<!--Helps with compatibility of the back to top link-->
<a id="readme-top"></a>

<!--PROJECT SHIELDS-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]

<!--Project header-->
<br>
<div align="center">
  <h1 align="center">Plex File Organizer</h1>
</div>

<!--Table of Contents-->
<details>
    <summary>Table of Contents</summary>
    <ol>
        <li><a href="#about-the-project">About The Project</a></li>
        <li><a href="#built-with">Built With</a></li>
        <li><a href="#running-the-program">Running the Program</a></li>
        <li><a href="#roadmap">RoadMap</a></li>
        <li><a href="#license">License</a></li>
        <li><a href="#Contact">Contact</a></li>
        <li><a href="#acknowledgements">Acknowledgments</a></li>
    </ol>
</details>

<!--ABOUT THE PROJECT -->
## About The Project
Creating a program to help the user create folder for new movies/tv shows, properly name media file(s) to match the media they are in while following
Plex approve file naming convention, and organize the media folder(s)--AKA your music folder--if it gets out of hand. Also, it will contain other handy futures:
rename existing media file(s); and have a built-in media player so the user can see what the media file is, thus allowing them to name it properly.

<p align="right">(<a href="#readme-top">Back To Top</a>)</p>

<!--BUILT WITH-->
## Built With
* [![Python][python-shield]][python-url]
* [![Pyside6][pyside-shield]][pyside-url]

<p align="right">(<a href="#readme-top">Back To Top</a>)</p>

<!--Running the Program-->
## Running the Program
Download a copy of the repo to your local computer, open it in your favorite IDE/IDLE, download the necessary library(s)
listed below:
* PySide 6

Once you have the listed library(s) installed simply run the setup.py. It should start right up.

If you wish to make an executable, download the latest version of PyInstaller, open a terminal, navigate to where the project
folder is located, and then run the follow commanded in the terminal.

<code>
pyinstaller plex-file-organizer.spec
</code>

<p align="right">(<a href="#readme-top">Back To Top</a>)</p>

<!-- ROADMAP -->
## Roadmap
_Version 1 Features_
- [x] Create a media folder for a new movie or TV show, along with sub-folders for miscellaneous content--trailers, extra, etc.
- [ ] Add a new season folder to an existing TV show media folder.
- [ ] Automatically go through the selected folder and identify the media files that need to be updated and rename the file accordingly.
  - [ ] know what episode number to start from for new media files if there are existing ones already in the folder.
- [ ] Allow the user to manually rename media files--new or existing--in an existing folder.

_Version 2 Features_
- [ ] Built in media player to allow user to watch to see which episode the media file is.

_Version 3 Features_
- [ ] Organize the media folder--AKA, the music folder.

Will work on getting these added to Github Issue section. For now, the up-and-coming features reside here.

**NOTE** If you look at the history of this project, you will notice a commit that say "Version 2.0.0". Please ignore that.
When I realized that I wanted more features and make this repo public, I made the decision to start over at Version 1.0.0.

<!-- License -->
## License
Distributed under the GPL-3.0 License. See 'LICENSE.txt' for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- Contact -->
## Contact
Please head to my portfolio website and use the contact form to reach out to me:
[My Portfolio Website][portfolio-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [Choose an Open Source License](https://choosealicense.com)
* [Img Shields](https://shields.io)
* [Simple Icons](https://simpleicons.org/?q=py)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
[contributors-shield]: https://img.shields.io/github/contributors/ColorlessSaber/PlexFileOrganizer.svg?style=for-the-badge
[contributors-url]: https://github.com/ColorlessSaber/PlexFileOrganizer/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/ColorlessSaber/PlexFileOrganizer.svg?style=for-the-badge
[forks-url]: https://github.com/ColorlessSaber/PlexFileOrganizer/network/members
[stars-shield]: https://img.shields.io/github/stars/ColorlessSaber/PlexFileOrganizer.svg?style=for-the-badge
[stars-url]: https://github.com/ColorlessSaber/PlexFileOrganizer/stargazers
[issues-shield]: https://img.shields.io/github/issues/ColorlessSaber/PlexFileOrganizer.svg?style=for-the-badge
[issues-url]: https://github.com/ColorlessSaber/PlexFileOrganizer/issues

[python-shield]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
[python-url]: https://www.python.org
[pyside-shield]: https://img.shields.io/badge/pyside6-4ED980?style=for-the-badge
[pyside-url]: https://wiki.qt.io/Qt_for_Python
[pyinstaller-url]: https://pyinstaller.org/en/stable/

[portfolio-url]: https://colorlesssaber.github.io/