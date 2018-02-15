import base.logix as d
import base.models.mcube as c
import base.Vector3D as v
from tkinter import *
import time as t

divjok = d.Divjok()
cube = c.Rectangle(v.Vector3D(0, 0, 0), v.Vector3D(300, 300, 10))
cube1 = c.Rectangle(v.Vector3D(0, 150, 0), v.Vector3D(100, 100, 5))
divjok.add_to_draw(cube)
divjok.add_to_draw(cube1)
for i in range(0, 360):
    cube.rotate_y(1)
    cube1.rotate_y(-1)
    divjok.clear_canvas()
    divjok.create_coordinate_axis()
    divjok.draw()
    divjok.update()

#--------REQUIRED TASK---------
divjok.loop()
#------------------------------
