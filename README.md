# biocResort LC-MS/MS helper

Biocrates allows for multiple injections per well such as quality controls but puts them all right after each other in the injection sequence. Usually this is not how one would like them to be ordered but rather between batches of normal sample inejctions. This script automates that resorting for you with a number of options that you can control via a configuration file.

The code is foreseen to be compiled into a windows executable where injection files can be dragged and dropped on top of it, resorted and saved under a new name in the same location as the original file.

