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


def create_line(x1, y1, x2, y2, arrow='none', color="black", width=1):
    canvas.create_line(width2 + x1, height2 - y1, width2 + x2, height2 - y2, arrow=arrow, fill=color, width=width)


def create_line_vector(vector1, vector2, arrow='none'):
    create_line(vector1.x, vector1.y, vector2.x, vector2.y, arrow, color="red", width=2)


def create_text(x1, y1, caption):
    canvas.create_text(width2 + x1, height2 - y1, text=caption, font=("Purisa", 8))


def create_text_vector(vector, caption, x=0, y=0):
    create_text(vector.x + x, vector.y + y, caption=caption)


v3d_0 = v.Vector3D(0, 0, 0).to_isometric()
v3d_x = v.Vector3D(200, 0, 0).to_isometric()
v3d_y = v.Vector3D(0, 200, 0).to_isometric()
v3d_z = v.Vector3D(0, 0, 200).to_isometric()

print('v3d_x', v3d_x)
print('v3d_y', v3d_y)
print('v3d_z', v3d_z)

master = Tk()
master.geometry("{0}x{1}+300+200".format(width, height))
canvas = Canvas(master, width=width, height=height, bg="white")


def create_coordinate_axis():
    """Coordinate axis"""
    create_line(v3d_0.x, v3d_0.y, v3d_x.x, v3d_x.y, arrow="last")
    create_line(v3d_0.x, v3d_0.y, v3d_y.x, v3d_y.y, arrow="last")
    create_line(v3d_0.x, v3d_0.z, v3d_z.x, v3d_z.y, arrow="last")

    """Coordinate axis caption"""
    create_text(v3d_x.x, v3d_x.y + 10, caption="x")
    create_text(v3d_y.x, v3d_y.y + 10, caption="y")
    create_text(v3d_z.x, v3d_z.y + 10, caption="z")

def create_axis_values():
    for value in range(-250, 250, 10):
        create_text_vector(v.Vector3D(value, 0, 0).to_isometric(), y = 5, caption=StringVar(value))
        create_text_vector(v.Vector3D(0, value, 0).to_isometric(), y = 5, caption=StringVar(value))
        create_text_vector(v.Vector3D(0, 0, value).to_isometric(), y = 5, caption=StringVar(value))


create_coordinate_axis()

canvas.pack()

for i in range(360*2):
    canvas.delete("all")
    create_coordinate_axis()

    for value in range(0, 250, 25):
        create_text_vector(v.Vector3D(value, 0, 0).to_isometric(), y = 5, caption=value)
        create_text_vector(v.Vector3D(0, value, 0).to_isometric(), y = 5, caption=value)
        create_text_vector(v.Vector3D(0, 0, value).to_isometric(), y = 5, caption=value)

    # -----------------------------------------------------------------
    # Cube vectors
    lenc = 100

    # vc1 = v.Vector3D(0, 0, 0)       .translate(0, 0, 0) .rotateY(i) .to_isometric()
    # vc2 = v.Vector3D(0, lenc, 0)    .translate(0, 0, 0) .rotateY(i) .to_isometric()
    #
    # vc3 = v.Vector3D(0, lenc, lenc)         .translate(0, 0, 0) .rotateY(i) .to_isometric()    #.rotateY(i)    #.rotate_around_point(i, vc1)
    # vc4 = v.Vector3D(0, 0, lenc)            .translate(0, 0, 0) .rotateY(i) .to_isometric()    #.rotateY(i)    #.rotate_around_point(i, vc1)
    # vc5 = v.Vector3D(lenc, 0, lenc)         .translate(0, 0, 0) .rotateY(i) .to_isometric()    #.rotateY(i)    #.rotate_around_point(i, vc1)
    # vc6 = v.Vector3D(lenc, 0, 0)            .translate(0, 0, 0) .rotateY(i) .to_isometric()    #.rotateY(i)    #.rotate_around_point(i, vc1)
    # vc7 = v.Vector3D(lenc, lenc, 0)         .translate(0, 0, 0) .rotateY(i) .to_isometric()    #.rotateY(i)    #.rotate_around_point(i, vc2)
    # vc8 = v.Vector3D(lenc, lenc, lenc)      .translate(0, 0, 0) .rotateY(i) .to_isometric()    #.rotateY(i)    #.rotate_around_point(i, vc2)

    # create_text_vector(vc1, "1", 5, 5)
    # create_text_vector(vc2, "2", 5, 5)
    # create_text_vector(vc3, "3", 5, 5)
    # create_text_vector(vc4, "4", 5, 5)
    # create_text_vector(vc5, "5", 5, 5)
    # create_text_vector(vc6, "6", 5, 5)
    # create_text_vector(vc7, "7", 5, 5)
    # create_text_vector(vc8, "8", 5, 5)

    # create_line_vector(vc1, vc2)
    # create_line_vector(vc3, vc4)
    # create_line_vector(vc1, vc4)
    # create_line_vector(vc2, vc3)
    # create_line_vector(vc2, vc7)
    # create_line_vector(vc1, vc6)
    # create_line_vector(vc7, vc6)
    # create_line_vector(vc7, vc8)
    # create_line_vector(vc8, vc5)
    # create_line_vector(vc4, vc5)
    # create_line_vector(vc6, vc5)
    # create_line_vector(vc3, vc8)

    # ------------------------------------------------------------------------------


    # Mechanic manipulator---------------------------------------


    l1 = v.Vector3D(0, 50, 0)
    l2 = v.Vector3D(-50, 50, 0).rotateY(i)
    create_line_vector(l1.to_isometric(), l2.to_isometric())

    m1 = v.Vector3D(-50, 50, 0).rotateY(i)
    m2 = v.Vector3D(-50, 50, -50).rotateX(i).rotateY(i)
    create_line_vector(m1.to_isometric(), m2.to_isometric(), arrow="last")

    # x = 75
    # z = 75
    # y = 25
    # on_x_axis1 = v.Vector3D(x, y, 0)
    # on_x_axis2 = v.Vector3D(x, y, z).rotateX(i)
    # create_line_vector(on_x_axis1.to_isometric(), on_x_axis2.to_isometric(), arrow="last")


    # -----------------------------------------------------------
    master.update()
    # time.sleep(0.001)

master.mainloop()
