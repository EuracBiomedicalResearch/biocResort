# biocResort LC-MS/MS helper

Biocrates allows for multiple injections per well in their workflow but puts them all right after each other in the injection sequence. This is not so ideal when wanting to inject QC samples between every x injections of samples. This script automates that resorting for you with a number of options that you can control via a configuration file (resort.ini)

The code is foreseen to be compiled into a windows executable where injection files can be dragged and dropped on top of it, resorted and saved under a new name (adding 'resorted' to the end of the name) in the same location as the original file.

To build the executable install pyinstaller (http://www.pyinstaller.org/ ) and run it with the command line options shown in the toBuild.txt file. As you see from the toBuild file it assumes win32 versions of both python 2.7 and the pyinstaller in this instance. It has given us better results than the 64 bit versions. Your milage may be different in this regard.

In the resort.ini file you should find explanations of what can be put in there and the options around them. Briefly it is split in two main sections, one is the sequence at the beginning of the run and one is the sequence that happens every x injections. For both sections you need to explicitly tell the pogram how to behave. This means you need to tell it that the blank and the BSA and the calibrants should be in the beginning sequence and you should see how the resort.ini file supplied.

For the sequence between sample injections you have control over how many sample injections are performed between the control sequence and also what samples are included in the control sequence. 

Both instances take into account that you might have the same sample ID in more than one well on your plate and you have options to control what happens in this case.
