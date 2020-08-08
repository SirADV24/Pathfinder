# Python Search/Pathfinder

# Overview 

I managed to create this tool that allow the visualisation of the most common pathfidner/grid search algorythms.

# Examples
- Short video: [Demo](https://www.youtube.com/watch?v=bW9yDvDNpE0&feature=youtu.be)
- Also Exampe folder

# Tutorial

Run main.py

- From the menu the user can customise the search algorythm / Heuristic function if the algorythm uses one / Grid size / Allowed directions
- Left click to draw on the grid
- Right click to erase from the grid
- M to open the menu again
- R to restart ( return to the original state of the grid )
- Space to start the animation
- G to generate a random maze 


# Aproach

Interface - PyGame

Everything related to the interface is made with the help of pygame .
- To draw the grid i choose to not draw it in the classical way ( drawing n x m lines ) but to draw the grid for every cell in particular.
  Every cell will draw it's color in a py.Rect and also draw its borders. I have choosen this aproach because if you paint something over the
  grid ( in way the grid is no longer visible ) you don't have to redraw the whole grid ( I ran into this problem while painting the cells, the
  cell will overlap the grid ) . With this aproach you can't overlap with the grid ( borders are drawned after the cell have been filled )
 
 Logic -
 
 Service class serves the purpose of holding everyone togheter
 - Comunicates to the database to get the cell objects 
 - Comunicates to the pathfinders to actually get the shortest path and to draw on the screen
 - Comunicates to the maze generator to .. generate the maze
 
 Data -
 
 I started to the idea that the cells might be anything ( like GPS cells or something ) in the future , so i implemented a mini-in-memory data base
 You can use a list and get the same result.
 
 # Animation
 
 To achive the animation , we perform the algorythm, calling the function draw whenever we find it necessary . Draw function is a lambda defined function
 from the Interface that is given as parameter to the service

 
 
 
