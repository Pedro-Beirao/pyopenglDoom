# Guide on how to use glBSP

Doom maps need nodes to be created in order to be able to display them correctly. Since this project uses OpenGL, an extra set of nodes needs to be created. These are called GL nodes.

To create these nodes, we need a GL friendly node builder such as glBSP, Zennode or ZDBSP. This guide will show how to use glBSP

### 1 - Download glBSP

glBSP works on Windows Linux and MacOS

Binaries for the Windows and Linux (x86) are available in http://glbsp.sourceforge.net/download.php

As I couldn't find binaries anywhere for MacOS, I decided to compile it myself. You can download it in [Releases](https://github.com/Pedro-Beirao/pyopenglDoomRenderer/releases)

### 2 - Use glBSP

1. Open the Teminal/CMD
2. Drag the glBSP.exe into the window
3. Drag the WAD file you want to write GL nodes to, into the window
```
C:\\path\to\glBSP.exe C:\path\to\doom.wad
```
This will create a .gwa file, it contains our precious GL nodes

Make sure that the WAD file and the .gwa file are in the same directory and have the same name, before running the renderer.
