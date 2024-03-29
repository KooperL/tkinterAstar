import tkinter as tk
from tkinter import *
#import random

size = 30       # Size of window
movement_options = [(0, -1), (0, 1), (-1, 0), (1, 0)]
#random.shuffle(movement_options)
matrix_size_var = int(size/3)
x_matrix = []
y_matrix = []
ignore = { 40 : None, 41 : None} # Ascii

class Node():
  def __init__(self, parent=None, position=None):
    self.parent = parent
    self.position = position
    self.g = 0                                                                              # Cost of the current path/node from the starting node
    self.h = 0                                                                              # Estimated cost of current path to end node
    self.f = 0                                                                              # Sum of g and h

  def __eq__(self, other):
    return self.position == other.position

  
def create_grid(event=None):
  global y_matrix
  global x_matrix
  global backend_matrix
  yticker = 0
  xticker = 0
  y_matrix = []
  x_matrix = []
  w = c.winfo_width()
  h = c.winfo_height()
  c.delete('grid_line')                                                                     # Will only remove objects with the ID: grid_line

  for i in range(0, int(w-size/3), size):
    c.create_line([(i, 0), (i, h)], tag='grid_line')                                        # Creates all vertical lines at intevals of size (window height)
    y_matrix.append(i)                                                                      # Replace all in column yticker with current i. This creates a coordinate system
    yticker += 1                                                                            # update ticker to view next
#   print(y_matrix)
    
  for i in range(0, int(h-size/3), size):
    c.create_line([(0, i), (w, i)], tag='grid_line')                                        # Same as above
    x_matrix.append(i)                 
    xticker += 1
#   print(x_matrix)

  backend_matrix = [[0 for x in x_matrix] for y in y_matrix]
#   print(backend_matrix)


    
def mouse_click(e):
  global x_start
  global y_start
  global x_stop
  global y_stop
  global backend_matrix
  x_coord_snap = None
  y_coord_snap = None

  for ia in x_matrix:  #
    if ia <= e.x < ia + size:                                                               # BUG: Clicks cant go beyond 10?
      x_coord_snap = ia  #
  for ia in y_matrix:                                                                       # Create a loop which is as long as the matrix's width. Need i to search column-by-column
    if ia <= e.y < ia + size:                                                               # If the current mouse coords are greater than this coord, and less than this coord + square size...
      y_coord_snap = ia                                                                     # Update this string to make the square snap to the corner

#   print("-")
#   print("x: {}".format(x_coord_snap/size))
#   print("y: {}".format(y_coord_snap/size))
#   print("-")

  ## TODO: Use switch/case once it is added in standard python library
  if click_var.get() == 1:
    c.delete('start')
    c.create_rectangle(x_coord_snap, y_coord_snap, x_coord_snap + size, y_coord_snap + size, width=2, outline='', fill='green', tag=('block', 'start'))
    x_start = int(x_coord_snap/size)
    y_start = int(y_coord_snap/size)
  elif click_var.get() == 2:
    c.delete('stop')
    c.create_rectangle(x_coord_snap, y_coord_snap, x_coord_snap + size, y_coord_snap + size, width=2, outline='', fill='red', tag=('block', 'stop'))
    x_stop = int(x_coord_snap/size)
    y_stop = int(y_coord_snap/size)
  elif click_var.get() == 3:
    c.create_rectangle(x_coord_snap, y_coord_snap, x_coord_snap + size, y_coord_snap + size, width=2, outline='', fill='black', tag=('block', 'object'))
    backend_matrix[int(x_coord_snap/size)][int(y_coord_snap/size)] = 1
    # print("-")
    # print("Matrix: ")         
    # for i in backend_matrix:
    #   print(i, "\n")
    # print("-")

def clear():
  for i in backend_matrix:
    i = 0
  c.delete('block')
  print("-----------------------------")
  print("-----------------------------")
  print(backend_matrix)


def pathfind():
  maze = backend_matrix
  start = (x_start, y_start)
  end = (x_stop, y_stop)
  c.delete('start', 'stop', 'path', 'nodes')
  path = astar(maze, start, end)
  c.tag_raise('object')
  c.create_rectangle(x_start * size, y_start * size, x_start * size + size, y_start * size + size, width=2, outline='black', fill='green', tag=('block', 'start'))
  c.create_rectangle(x_stop * size, y_stop * size, x_stop * size + size, y_stop * size + size, width=2, outline='black', fill='red', tag=('block', 'stop'))
  print(path)

def pathfinddebug():
  maze = [[0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
      [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 1, 0, 0, 0, 0, 0]]
  print(maze)
  start = (0, 0)
  end = (5, 0)
  path = astar(maze, start, end)
  print(path)

def astar(maze, start, end):
  start_node = Node(None, start)
  start_node.g = start_node.h = start_node.f = 0
  end_node = Node(None, end)
  end_node.g = end_node.h = end_node.f = 0

  open_list = []
  closed_list = []
  history_list = []
  open_list.append(start_node)

  ## Iterate through list of children
  while len(open_list) > 0:
    current_node = open_list[0]
    current_index = 0
    for index, item in enumerate(open_list):
      if item.f < current_node.f:
        current_node = item
        current_index = index

    ## Check if correct:
    open_list.pop(current_index)
    closed_list.append(current_node)
    if current_node == end_node:
      path = []
      current = current_node
      while current is not None:
        path.append(current.position)
        current = current.parent
        #print(path)
        for i in list(path[::-1]):
          i = str(i).split(", ")
          c.create_rectangle(int(i[0].translate(ignore)) * size, int(i[1].translate(ignore)) * size, int(i[0].translate(ignore)) * size + size, int(i[1].translate(ignore)) * size + size, width=2, outline='black', fill='blue', tag=('block', 'path'))
      return "Path: ", path[::-1]

    ## Check if legal child can be created:
    children = []
    for new_position in movement_options:
      node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])
      if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
        continue

      if maze[node_position[0]][node_position[1]] != 0:
        continue

      ## Create new node, with current node as parent
      new_node = Node(current_node, node_position)
    #   print(new_node.position)

      if new_node in children:
        continue
      if new_node in history_list:
        continue
      children.append(new_node)
      history_list.append(new_node)


      display_reach = str(node_position).split(", ")
      c.create_rectangle(int(display_reach[0].translate(ignore)) * size, int(display_reach[1].translate(ignore)) * size, int(display_reach[0].translate(ignore)) * size + size, int(display_reach[1].translate(ignore)) * size + size, width=2, outline='', fill='teal', tag=('block', 'nodes'))
    # print("----")

    ## Configure child with cost parameters:
    for child in children:
      for closed_child in closed_list:
        if child == closed_child:
          continue

      child.g = current_node.g + 1
      child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
      child.f = child.g + child.h

      for open_node in open_list:
        if child == open_node and child.g > open_node.g:
          continue
      open_list.append(child)
      
## Instanciate window
root = tk.Tk()
root.title("PathFinder A*")
c = tk.Canvas(root, height=size*10, width=size*10, bg='white')
#c.pack(fill=tk.BOTH, expand=True)
c.grid(row=0,column=0,rowspan=size, sticky=NW)

c.bind('<Configure>', create_grid)
c.bind('<Button-1>', mouse_click)

btn_clear = tk.Button(root, text="Clear", width=25, height=2, command=clear)
btn_pathfind = tk.Button(root, text="Path find", width=25, height=2, command=pathfind)


click_var = IntVar()
rad_start = Radiobutton(root,text='Start', value=1, variable=click_var)
rad_stop = Radiobutton(root,text='Stop', value=2, variable=click_var)
rad_obj = Radiobutton(root,text='Object', value=3, variable=click_var)
rad_start.grid(row=0,column=1)
rad_stop.grid(row=1,column=1)
rad_obj.grid(row=2,column=1)

btn_clear.grid(row=size-2,column=1)
btn_pathfind.grid(row=size-1,column=1)

root.mainloop()
