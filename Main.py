import base.matrixutils as utils
from tkinter import *
import time
import base.Vector3D as v

# A = utils.to_matrix(2, [2, 2, 2, 2])
# B = utils.to_matrix(1, [5, 5])
#
# # print('A:', A)
# # print('B:', B)
# print(utils.matrixmult(A, B))

width = 500
height = 500
width2 = float(width / 2)
height2 = float(height / 2)


def create_line(x1, y1, x2, y2, arrow='none'):
    canvas.create_line(width2 + x1, height2 - y1, width2 + x2, height2 - y2, arrow=arrow)


def create_line_vector(vector1, vector2, arrow='none'):
    create_line(vector1.x, vector1.y, vector2.x, vector2.y, arrow)


def create_text(x1, y1, caption):
    canvas.create_text(width2 + x1, height2 - y1, text=caption)


v3d_0 = v.Vector3D(0, 0, 0).to_isometric()
v3d_x = v.Vector3D(200, 0, 0).to_isometric()
v3d_y = v.Vector3D(0, 200, 0).to_isometric()
v3d_z = v.Vector3D(0, 0, 200).to_isometric()

v3d_1 = v.Vector3D(50, 50, 0).to_isometric().rotate_y(65)
v3d_2 = v.Vector3D(0, 50, 50).to_isometric().rotate_y(65)

print('v3d_x', v3d_x)
print('v3d_y', v3d_y)
print('v3d_z', v3d_z)

master = Tk()
master.geometry("{0}x{1}+300+200".format(width, height))

canvas = Canvas(master, width=width, height=height, bg="white")

create_line(v3d_0.x, v3d_0.y, v3d_x.x, v3d_x.y, arrow="last")
create_line(v3d_0.x, v3d_0.y, v3d_y.x, v3d_y.y, arrow="last")
create_line(v3d_0.x, v3d_0.z, v3d_z.x, v3d_z.y, arrow="last")

create_line_vector(v3d_1, v3d_2)
create_line_vector(v3d_z, v3d_x)







# canvas.create_line(w2 - v3d_0.x, h2 - v3d_0.y, w2 - v3d_x.x, h2 - v3d_x.y, arrow="last")
# canvas.create_line(w2 - v3d_0.x, h2 - v3d_0.y, w2 - v3d_y.x, h2 - v3d_y.y, arrow="last")
# canvas.create_line(w2 - v3d_0.x, h2 - v3d_0.y, w2 - v3d_z.x, h2 - v3d_z.y, arrow="last")
#
create_text(v3d_x.x, v3d_x.y + 10, caption="x")
create_text(v3d_y.x, v3d_y.y + 10, caption="y")
create_text(v3d_z.x, v3d_z.y + 10, caption="z")



canvas.pack()
# canvas.mainloop()
master.mainloop()

for i in range(100):
    create_text(v3d_x.x, v3d_x.y + i, caption=i)
    time.sleep(0.1)
    canvas.pack()
    master.update_idletasks()
