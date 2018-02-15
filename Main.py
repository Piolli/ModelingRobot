import base.logix as d
import base.models.mcube as c
import base.Vector3D as v
from tkinter import *
import time as t

divjok = d.Divjok()
cube = c.Rectangle(v.Vector3D(0, 0, 0), v.Vector3D(300, 300, 10))
cube1 = c.Rectangle(v.Vector3D(0, 150, 0), v.Vector3D(100, 100, 5))
# divjok.add_to_draw(cube)
# divjok.add_to_draw(cube1)
for i in range(0, 1):
    cube.rotate_y(1)
    cube1.rotate_y(-1)
    divjok.clear_canvas()
    divjok.create_coordinate_axis()
    divjok.draw()
    divjok.update()

# --------REQUIRED TASK---------
top = Toplevel()
top.deiconify()
top.title("Add rectangle")

Label(top, text="Enter x1").grid(row=0, column=0)
Label(top, text="Enter y1").grid(row=0, column=1)
Label(top, text="Enter z1").grid(row=0, column=2)

rect_x1 = Entry(top)
rect_y1 = Entry(top)
rect_z1 = Entry(top)
rect_x1.grid(row=1, column=0)
rect_y1.grid(row=1, column=1)
rect_z1.grid(row=1, column=2)

Label(top, text="Enter x2").grid(row=2, column=0)
Label(top, text="Enter y2").grid(row=2, column=1)
Label(top, text="Enter z2").grid(row=2, column=2)

rect_x2 = Entry(top)
rect_y2 = Entry(top)
rect_z2 = Entry(top)
rect_x2.grid(row=3, column=0)
rect_y2.grid(row=3, column=1)
rect_z2.grid(row=3, column=2)


def callback():
    x1 = int(rect_x1.get())
    y1 = int(rect_y1.get())
    z1 = int(rect_z1.get())

    x2 = int(rect_x2.get())
    y2 = int(rect_y2.get())
    z2 = int(rect_z2.get())

    cube3 = c.Rectangle(v.Vector3D(x1, y1, z1), v.Vector3D(x2, y2, z2))
    divjok.add_to_draw(cube3)
    divjok.draw()



enter_data = Button(top, text="Enter", width=15, command=callback).grid(row=4, column=1)

divjok.loop()
# ------------------------------
