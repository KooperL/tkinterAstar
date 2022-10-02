# Important

This app uses `python 3.x`.

# About

This project demonstrates the A star algorithm in a DIY maze style path-finding app. This is done using the GUI library `tkinter` and object oriented programming. 

# Installation

`tkinter` is included in the standard library for `python 3.x`, so further installations are not needed.
Simply `python main.py` from the command line to run it.

# Getting started

After launching, use the radio buttons to create an object on the grid. There can only be a single `start` object, and a single `stop` object. Use the `object` object (yeah I know, it's on the TODO list) to create an obstacle on the grid.
Use the mouse and left mouse clicks to place objects.
Clear the grid with the `clear` button to redraw objects.
Select `path find` to run the algorithm and find the shortest path between the two nodes.
The turquoise squares are children that the algorithm considered taking the path of. Blue squares represent the official path.