from tkinter import *
import base.Vector3D as v


class Divjok:
    __models = list()
    __width = 500
    __height = 500
    __width2 = float(__width / 2)
    __height2 = float(__height / 2)

    def __init__(self) -> None:
        self.__master = Tk()
        self.__master.geometry("{0}x{1}+300+200".format(self.__width, self.__height))
        self.__canvas = Canvas(self.__master, width=self.__width, height=self.__height, bg="white")
        self.__canvas.pack()

    def create_line(self, x1: int, y1: int, x2: int, y2: int, arrow='none', color="black", width=1):
        self.__canvas.create_line(self.__width2 + x1, self.__height2 - y1, self.__width2 + x2, self.__height2 - y2,
                                  arrow=arrow, fill=color, width=width)

    def create_line_v(self, vector1: v, vector2: v, arrow='none'):
        self.create_line(vector1.x, vector1.y, vector2.x, vector2.y, arrow, color="red", width=2)

    def create_text(self, x1: int, y1: int, caption: str):
        self.__canvas.create_text(self.__width2 + x1, self.__height2 - y1, text=caption, font=("Calibri", 14))

    def create_text_v(self, vector: v, caption: str, x=0, y=0):
        self.create_text(vector.x + x, vector.y + y, caption=caption)

    def create_coordinate_axis(self):
        """Coordinate axis vectors"""
        v3d_0 = v.Vector3D(0, 0, 0).to_isometric()
        v3d_x = v.Vector3D(200, 0, 0).to_isometric()
        v3d_y = v.Vector3D(0, 200, 0).to_isometric()
        v3d_z = v.Vector3D(0, 0, 200).to_isometric()
        """Coordinate axis"""
        self.create_line(v3d_0.x, v3d_0.y, v3d_x.x, v3d_x.y, arrow="last")
        self.create_line(v3d_0.x, v3d_0.y, v3d_y.x, v3d_y.y, arrow="last")
        self.create_line(v3d_0.x, v3d_0.z, v3d_z.x, v3d_z.y, arrow="last")
        """Coordinate axis caption"""
        self.create_text(v3d_x.x, v3d_x.y + 10, caption="x")
        self.create_text(v3d_y.x, v3d_y.y + 10, caption="y")
        self.create_text(v3d_z.x, v3d_z.y + 10, caption="z")

    def create_axis_values(self):
        for value in range(-250, 250, 10):
            self.create_text_v(v.Vector3D(value, 0, 0).to_isometric(), y=5, caption=StringVar(value))
            self.create_text_v(v.Vector3D(0, value, 0).to_isometric(), y=5, caption=StringVar(value))
            self.create_text_v(v.Vector3D(0, 0, value).to_isometric(), y=5, caption=StringVar(value))

    def clear_canvas(self):
        self.__canvas.delete("all")

    def create_cube(self):
        cube_length = 100

        vc1 = v.Vector3D(0, 0, 0).to_isometric()
        vc2 = v.Vector3D(0, cube_length, 0).to_isometric()

        vc3 = v.Vector3D(0, cube_length, cube_length).to_isometric()
        vc4 = v.Vector3D(0, 0, cube_length).to_isometric()
        vc5 = v.Vector3D(cube_length, 0, cube_length).to_isometric()
        vc6 = v.Vector3D(cube_length, 0, 0).to_isometric()
        vc7 = v.Vector3D(cube_length, cube_length, 0).to_isometric()
        vc8 = v.Vector3D(cube_length, cube_length, cube_length).to_isometric()

        self.create_text_v(vc1, "1", 5, 5)
        self.create_text_v(vc2, "2", 5, 5)
        self.create_text_v(vc3, "3", 5, 5)
        self.create_text_v(vc4, "4", 5, 5)
        self.create_text_v(vc5, "5", 5, 5)
        self.create_text_v(vc6, "6", 5, 5)
        self.create_text_v(vc7, "7", 5, 5)
        self.create_text_v(vc8, "8", 5, 5)

        self.create_line_v(vc1, vc2)
        self.create_line_v(vc3, vc4)
        self.create_line_v(vc1, vc4)
        self.create_line_v(vc2, vc3)
        self.create_line_v(vc2, vc7)
        self.create_line_v(vc1, vc6)
        self.create_line_v(vc7, vc6)
        self.create_line_v(vc7, vc8)
        self.create_line_v(vc8, vc5)
        self.create_line_v(vc4, vc5)
        self.create_line_v(vc6, vc5)
        self.create_line_v(vc3, vc8)

    def create_manipulator(self, i):
        l1 = v.Vector3D(0, 50, 0)
        l2 = v.Vector3D(-50, 50, 0).rotateY(i)
        self.create_line_v(l1.to_isometric(), l2.to_isometric())

        m1 = v.Vector3D(-50, 50, 0).rotateY(i)
        m2 = v.Vector3D(-50, 50, -50).rotateX(i).rotateY(i)
        self.create_line_v(m1.to_isometric(), m2.to_isometric(), arrow="last")

    def add_to_draw(self, model):
        self.__models.append(model)

    def update(self):
        self.__master.update()

    def loop(self):
        self.__master.mainloop()

    def draw(self):
        for model in self.__models:
            model.draw(self)
        self.__master.update()
