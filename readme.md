# QTPY LFO

Inspired by Ochd

https://divkidvideo.com/ochd-the-second-divkid-eurorack-module/

This only has 4, and was more of a means to build something with a DAC and the RP2040.  I would say if you want 8 LFOs, get that, otherwise this could fit some similar tickboxes.

This "journey" has 4 parts, so do not consider this a standalone project that you can just build from.  Im not supporting this, just taking notes.

## First Schematic

The First schematic is what I do in easyeda.  I generally sketch out the idea and then split it into two parts.  Top and Bottom each ultimately has its own project.  I have not really figured out how to master that tool yet.  Meh.

## Second pass.  What I actually built

The Second pass had some bugs.  Mostly the pots were hooked up to 5v instead of 3.3.  Opps.  That was the run I made and I fixed it on the fly.  The schematics had some bugs ( I fixed em) so Im not including them.

I also squeezed in a neopixel after the fact.  It looks nice and displays the scene. 

## Main Schematics that I have posted

The Main schematics should be considered untested, but if I were to do another run, this might be what I use.

## TODO - Just a code example and breadboard tested.

The final arduino code would be for a schematic that does not exist.  I would say the final incarnation would be to ditch the op amp and 4 leds and just use neopixels.  The code is there for that. It works on a bread board.

The design really in that case would just be the QT, DAC, some pull up resistors and thats about it.

I will link to the project and add the final gerbers, but keep in mind, I have not built from the final gerbers. They are as is.

And I really would like to do this again without the LEDs and just use neopixels.  The code for that is same circuit python directory/lib, but just swap out the code in python-vx.




