# biocResort LC-MS/MS helper

Biocrates allows for multiple injections per well such as quality controls but puts them all right after each other in the injection sequence. Usually this is not how one would like them to be ordered but rather between batches of normal sample inejctions. This script automates that resorting for you with a number of options that you can control via a configuration file.

The code is foreseen to be compiled into a windows executable where injection files can be dragged and dropped on top of it, resorted and saved under a new name in the same location as the original file.

To build the executable install pyinstaller (http://www.pyinstaller.org/ ) and run it with the command line options shown in the toBuild.txt file. As you see from the toBuild file I work with win32 versions of both python 2.7 and the pyinstaller in this instance. It has given me better results than the 64 bit versions. Your milage may be different in this regard.

In the resort.ini file you should find explanations of what can be put in there and the options around them.
