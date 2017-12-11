# Youtube Music Player

It has been written in python3. It is a CLI music player that  downloads audios from youtube videos, and then plays them.

Also It works with youtube lists.


## Dependencies

  * [VLC](https://www.videolan.org/vlc/index.es.html)
  * [python3](https://www.python.org/downloads/)
  * pip3

## Installation

### Linux
 1. Install VLC player, python 3, pip3 and virtualenv.
 2. Download the project.
 3. Give execution permissions to all scripts that are in linux folder (`chmod +x ./linux/*`).
 4. Open linux folder in console (`cd ./linux`).
 5. Execute the script named **create-virtenv.sh** (`./create-virtenv.sh`) to create the virtual enviroment, where all dependencies will be installed.
 6. Execute the script named **install-dependencies.sh** (`./install-dependencies.sh`) to install required dependencies, that are defined in **requirements.txt**.

### Windows
  1. Install VLC player and a release of python3 with pip3.
   * Make sure the option "Add Python to environment variables" is checked in the step named *Advanced Options* of the python3 installation wizard.  
  2. Download the project.
  3. Execute the script named **install-dependencies.bat**, that is in windows folder. And it will install dependencies of **requirements.txt** file.





## List of youtube videos

It is necessary a text file with all urls of youtube videos that you want to play.

EXAMPLE
```
https://www.youtube.com/watch?v=jgpJVI3tDbY
https://www.youtube.com/watch?v=8Z5EjAmZS1o
https://www.youtube.com/watch?v=d7hVQpyKLGg
```
You should name the file urls.list.

In windows It is mandatory that the encoding format be ANSI.

## Configuring Player
The configuration of the player is in the file **youtubePlayer.conf**.

By default this file contains this:
```
[youtubePlayerConfiguration]
urlFile=./urls.list
audioFolder=./audio
loop=true
random=true
```
  * The field **urlFile** contains the path to file that contains the list with urls of youtube.
  * The field **audioFolder** contains the path where music downloaded will be saved.
  * The field **random** is a boolean value that plays the list of music randomly (true) or according to the order of the file defined in urlFile (false).

## Execution
### Linux
  1. Open the console in linux folder.
  2. Execute exec.sh script.

If you want to add this script as usable command in your console, you will edit the file `~/.bashrc` and add to the end of the file the next line `alias youtube-player='cd /path/of/your/installation/youtube_music_player/linux;./exec.sh'`.

### Windows
Execute the script `./windows/exec.bat`.


## Development status
Now this project is in beta, the management of signals to properly close resources is not yet implemented.

And in a future I want to implement a GUI.
## Contributors
I want to thank the creators of VLC ([VideoLan](https://www.videolan.org/index.es.html)),
pafy library ( [mps-youtube](https://github.com/mps-youtube)) and [youtube-dl library](https://rg3.github.io/youtube-dl/about.html).


Any contributions are highly appreciated. The best way to contribute code is to open a
[pull request on gitHub](https://help.github.com/articles/about-pull-requests/).

## License
GPL v3 License.
