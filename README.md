# universalSoundBoard
A "Sound-Board" Python-script to annoy my Professors during Lecture.<br>
One of the Goals of this Project is to get a bit more familiar with Python, since i need to learn about this language for a Module.

## Features:
- Automatically adjusts the [volume](#command-line-arguments) to play the sound, regardless of your current volume (currently only on Linux)
- Window is always on top of other windows
- One Button can play different sounds
- Window can [align](#command-line-arguments) itself on the right, left or bottom

## Library Requirements:
- tkinter (through ```apt-get install python-tk``` or ```apt-get install python3-tk```)
- screeninfo
- playsound

## "Installing" the Program:
1. Download the [soundBoard Directory](./soundBoard)
2. Open the Terminal
3. Move into the downloaded soundBoard-Directory
4. Translate and Execute the Program via `python mySoundBoard.py [Argument] [Parameter]`

## Command-Line Arguments:
|Short Argument|Long Argument|Effect|Value-Range|
| :----------: | :---------: | :--: | :-------: |
|-h | --help | Displays Information about the Arguments | --- |
|-v | --volume | What the Volume is gonna be set to when a sound is played| 0 <= x <= 100 |
|-t | --text | The name of the Button from name of the directory<br> gets displayed beneath the Button | 0 == Don't display Text<br> 1 == Display Text|
|-a | --align | Centers the window to the right, left or to the Bottom of the screen | "right", "left", "bottom" (without qotation-marks) |

## Adding Sound-Buttons:
1. Create a Folder with a Name that matches the sound
2. Put Images for the pressed and unpressed Button as `pressedButton.png` and `unpressedButton.png` respectively into the created folder
3. Put at least one Sound in an .mp3 or .wav format into the created folder, when multiple Soundfiles are present it randomizes the sound
4. Drag the created Folder into the `soundBoard` Folder
5. Repeat the previous Steps for every sound-button you want to add

[Here are a few Ideas for Buttons](./SOUND_IDEAS.md)
