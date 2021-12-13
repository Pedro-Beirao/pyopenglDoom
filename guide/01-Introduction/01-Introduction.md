# 01-Introduction

This guide will go over the anatomy of a Doom WAD file, in particular the map Lumps

We will understand how to read data from a WAD file, how to get read the map Lumps (Vertexes, Sectors, etc), how to use GL nodes and render it all in OpenGL.

If you are looking for the actual raycast based renderer, see https://github.com/amroibrahim/DIYDoom

The whole code will be written in Python. We will use the Pygame and PyOpenGL libraries.

Requirements:
- Python 3 (Tested with Python 3.9)
    - MacOS: brew install python3
    - Windows: https://www.python.org/downloads/
    - Ubuntu: sudo apt-get install python3
- Pygame (Tested with Pygame 1.0.0)
    - MacOS / Linux: python3 -m pip install pygame
    - Windows: pip install pygame
- PyOpenGL (Tested with PyOpenGL 3.1.0)
    - MacOS / Linux: python3 -m pip install PyOpenGL
    - Windows: pip install PyOpenGL
    - (You can also install PyOpenGL-Accelerate, but in the way we will render, it does not make a difference)
- Some WAD file
    - You can get the free Shareware version of Doom from https://www.doomworld.com/idgames/idstuff/doom/doom19s
- glBSP (Tested with glBSP 2.4)
    - We will talk about this in a later chapter
- Slade3
    - Used to be able to visualize and edit the WAD file. http://slade.mancubus.net/index.php?page=downloads

Useful resources:
- Unnoficial Doom specs: https://www.gamers.org/dhs/helpdocs/dmsp1666.html
- Doomwiki: https://doomwiki.org/
- GL nodes specifications: http://glbsp.sourceforge.net/specs.php
- PrBoom-plus source code: https://github.com/coelckers/prboom-plus
- DIYDoom source code: https://github.com/amroibrahim/DIYDoom
- Doomworld: https://www.doomworld.com/forum/topic/126194-opengl-doom-renderer