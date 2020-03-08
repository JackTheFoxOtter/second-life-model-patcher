# Collada Model Patcher for Second Life

## What does it do?
This tool takes two input Collada files, determines the bounding boxes of both files, and (given that the secondary meshes bounding box is smaller than the first) artificially 'inflates' the bounding box of the secondary mesh by adding small, invisible "one-vertex triangles" to match the bounding box of the primary mesh.

## Why is it useful?
Second Life has the rather interesting quirk of always scaling secondary meshes to the same dimensions as the primary mesh when uploading a 3D object. This affects mesh collision boxes and custom LODs and ends in stretched results if the bounding boxes didn't line up perfectly before uploading. 
I suspect that this has been implemented to prevent objects from being used abusively (be it intentionally or by accident) by for example having the collision box of an object surpass the actual bounds of the object, leading to "invisible walls". This does - in a way - make a lot of sense, since it would negatively impact the player if they would constantly run into invisible walls / have the camera clip on them, however, it also penalizes creators like myself that try to create high quality and performant models. Spending hours of coming up with a nice asset creation workflow, just to realized everything looking rather ugly in-game after Second Life finished its adjustments.

## Usage
Once you start the tool, you will be able to enter two file paths (or use the handy file chooser by pressing the '...' buttons). These file paths should lead to your primary ('target bounding box size') and secondary ('geometry you want to have') Collada (.dae) files.
Once you select them, you should see their bounding boxes being displayed in the frame below.
Click the button to start the merging, and the tool will create and save a new file to the same folder of your secondary mesh (with the _patched postfix).
You're done! Congratulations

## How it works
The bounding box of an object can be described as 6 values, the largest and smallest occurrence of each axis (XYZ) in the positions of all vertices.
This tool simply injects either one or two additional vertices at the positions of the corner of the target bounding box to make the secondary mesh have the exact same bounds.
It then defines a 'triangle' for each added vertex (each 'corner' of the triangle is the same vertex) which effectively has a surface area of 0, making it invisible.

## Limitations
* No axis of the secondary object's bounding box may surpass the primary object's bounding box (secondary has to be smaller)
* Currently only Collada files that contain exactly one geometry are supported
* Second Life won't accept the result as a collision mesh because of the small triangle, however, the uploader can convert it to a hull, which validates it again and still maintains the scaling

## Installation
You will require two additional dependencies:
* [PyQt5](https://pypi.org/project/PyQt5/ "PyQt5 on PyPI"), responsible for the beautiful UI (`pip install PyQt5`)
* [pycollada](https://github.com/pycollada/pycollada "pycollada on GitHub"), responsible for reading, modifying and writing the Collada data (`pip install pycollada`)

## Future
As it stands right now, this tool is a stand-alone solution.
I am thinking of potentially embedding this functionality into a blender add-on, however, I am not sure if or when I'm going to tackle that.
