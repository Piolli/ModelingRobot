from tkinter import *
import base.Vector3D as v
import math as m
import base.logix as l
import operator


class ConfigurationSpace:
    def __init__(self, delta: int, width, height) -> None:
        self.__width = width
        self.__height = height
        self.__delta = delta

        self.__X0 = width / 2
        self.__Y0 = height / 2

        top = Toplevel()
        top.deiconify()
        top.title("Configuration space")
        top.geometry("{0}x{1}".format(self.__width, self.__height))
        self.__canvas = Canvas(top, width=self.__width, height=self.__height, bg="white")
        self.__canvas.pack()

    def draw_bg_lines(self):
        for i in range(0, self.__width, self.__delta):
            # Y axis
            self.__canvas.create_line(self.__X0 + i, 0, self.__X0 + i, self.__height)
            self.__canvas.create_line(self.__X0 - i, 0, self.__X0 - i, self.__height)

            # X axis
            self.__canvas.create_line(0, self.__Y0 + i, self.__width, self.__Y0 + i)
            self.__canvas.create_line(0, self.__Y0 - i, self.__width, self.__Y0 - i)

    def draw_axis(self):
        self.__canvas.create_line(0, self.__Y0, self.__width, self.__Y0, arrow='last', fill="red", width=3)
        self.__canvas.create_line(self.__X0, self.__height, self.__X0, 0, arrow='last', fill="red", width=3)

    def redraw(self):
        self.__canvas.delete("all")
        self.draw_axis()
        self.draw_bg_lines()

    def delta_window(self):
        top = Toplevel()
        top.deiconify()
        top.title("Set delta")

        Label(top, text="delta: ").grid(row=0, column=0)
        self.__delta_entry = Entry(top)
        self.__delta_entry.grid(row=0, column=1)

        Button(top, text="Set delta", command=self.delta_callback).grid(row=1, column=1)

    def delta_callback(self):
        delta = int(self.__delta_entry.get())
        self.__delta = delta
        self.redraw()

    def draw_point(self, x, y, color="blue"):
        size = 4
        mult_coef_x = self.__X0 / 180
        mult_coef_y = self.__Y0 / 180

        x *= mult_coef_x
        y *= mult_coef_y
        self.__canvas.create_oval(x - size + self.__X0, self.__Y0 - (y - size), x + size + self.__X0,
                                  self.__Y0 - (y + size), width=0, fill=color)
        # print(x - size + self.__X0, self.__Y0 - (y - size), x + size + self.__X0, self.__Y0 - (y + size))

    def draw_line(self, vector1: v.Vector3D, vector2: v.Vector3D):
        mult_coef_x = self.__X0 / 180
        mult_coef_y = self.__Y0 / 180

        vector1.x *= mult_coef_x
        vector1.y *= mult_coef_y

        vector2.x *= mult_coef_x
        vector2.y *= mult_coef_y

        self.__canvas.create_line(vector1.x + self.__X0, self.__Y0 - vector1.y, self.__X0 + vector2.x,
                                  self.__Y0 - vector2.y, width=2)

    def draw_line_for_manipulator(self, vector1: v.Vector3D, vector2: v.Vector3D):
        mult_coef_x = self.__X0 / 180
        mult_coef_y = self.__Y0 / 180

        # vector1.x *= mult_coef_x
        # vector1.y *= mult_coef_y

        vector2.x *= mult_coef_x
        vector2.y *= mult_coef_y

        self.__canvas.create_line(vector1.x + self.__X0, self.__Y0 - vector1.y, self.__X0 + vector2.x,
                                  self.__Y0 - vector2.y, width=2)

    def draw_intersection_line(self, vector1: v.Vector3D, vector2: v.Vector3D):
        coef = self.__delta * 180 / 800 * 2
        vector1.x *= coef
        vector1.y *= coef

        vector2.x *= coef
        vector2.y *= coef
        self.draw_line(vector1, vector2)

    def manipulator(self, a1: int, a2: int, L1: int, L2: int):
        Q1 = m.radians(a1)
        Q2 = m.radians(a2)

        # First vector from (0, 0)
        vA = v.Vector3D(0, 0, 0)
        vA.x = L1 * m.cos(Q1)
        vA.y = L1 * m.sin(Q1)

        # Second vector from end vA
        vS = v.Vector3D(0, 0, 0)
        vS.x = L2 * m.cos(Q1 + Q2) + vA.x
        vS.y = L2 * m.sin(Q1 + Q2) + vA.y

        return vA, vS

    def manipulator_window(self):

        top = Toplevel()
        top.deiconify()
        top.title("Add manipulator")

        q0_list = list()
        qt_list = list()
        Label(top, text="Введите число звеньев").grid(row=0, column=0)
        n = Entry(top)
        n.grid(row=0, column=1)

        Label(top, text="Введите q0").grid(row=1, column=0)
        Label(top, text="Введите qt").grid(row=1, column=1)

        q0_frame = Frame(top)
        qt_frame = Frame(top)
        q0_frame.grid(row=2, column=0)
        qt_frame.grid(row=2, column=1)

        def set_n_callback():
            q0_list.clear()
            qt_list.clear()

            nn = int(n.get())
            for widget in q0_frame.winfo_children():
                widget.destroy()
            for widget in qt_frame.winfo_children():
                widget.destroy()

            for i in range(nn):
                q0_entry = Entry(q0_frame)
                Label(q0_frame, text="Введите q0_" + str(i)).grid(row=i, column=0)
                q0_entry.grid(row=i, column=1)
                q0_list.append(q0_entry)

                qt_entry = Entry(qt_frame)
                Label(qt_frame, text="Введите qt_" + str(i)).grid(row=i, column=0)
                qt_entry.grid(row=i, column=1)
                qt_list.append(qt_entry)

        def draw_callback():
            if len(q0_list) == 2:
                v0 = v.Vector3D(0, 0, 0)
                v1, v2 = self.manipulator(int(q0_list[0].get()), int(q0_list[1].get()),
                                          int(qt_list[0].get()), int(qt_list[1].get()))
                self.draw_line_for_manipulator(v0, v1)
                self.draw_line_for_manipulator(v1, v2)

        Button(top, text="Set n", command=set_n_callback).grid(row=0, column=2)
        Button(top, text="Draw", command=draw_callback).grid(row=0, column=3)

    def draw_rectangle(self, vector1: v.Vector3D, vector2: v.Vector3D):
        # self.draw_line(v1, v1.translate(x=v2.x))
        # self.draw_line(v1, v1.translate(y=v2.y))
        # self.draw_line(v2, v2.translate(x=v1.x))
        # self.draw_line(v2, v2.translate(y=v1.y))
        mult_coef_x = self.__X0 / 180
        mult_coef_y = self.__Y0 / 180

        vector1.x *= mult_coef_x
        vector1.y *= mult_coef_y
        vector2.x *= mult_coef_x
        vector2.y *= mult_coef_y

        self.__canvas.create_rectangle(vector1.x + self.__X0, self.__Y0 - vector1.y, self.__X0 + vector2.x,
                                       self.__Y0 - vector2.y, width=3, fill="red")

    def draw_intersection_cell(self, cell_x, cell_y, color="red"):
        coef = self.__delta * 180 / 800 * 2
        self.draw_point(cell_x * coef, cell_y * coef, color)

    # Find next points on discrete space
    def find_next_points(self, start_point: ()):
        mapPointToDistance = {}

        def distance(point1: (), point2: ()):
            dist = 0
            for i in range(len(point1)):
                dist += (point2[i] - point1[i]) ** 2
            return round(m.sqrt(dist), 3)

        for point in self.get_all_points_of_space(start_point, 2):
            mapPointToDistance[point] = distance(point, start_point)

        sorted_x = sorted(mapPointToDistance.items(), key=operator.itemgetter(1))
        result_points = list()
        # print(sorted_x)
        for i in range(9):
            if sorted_x[i][0] != start_point:
                result_points.append(sorted_x[i][0])
            # self.draw_intersection_cell(sorted_x[i][0][0], sorted_x[i][0][1], color="none")

        return result_points

    def get_all_points_of_space(self, start_point, dimension: int):
        discrete_points = []
        delta = 5

        if dimension == 2:
            for x in range(start_point[0] - delta, start_point[0] + delta):
                for y in range(start_point[1] - delta, start_point[1] + delta):
                    discrete_points.append((x, y))
        if dimension == 3:
            for x in range(start_point[0] - delta, start_point[0] + delta):
                for y in range(start_point[1] - delta, start_point[1] + delta):
                    for z in range(start_point[2] - delta, start_point[2] + delta):
                        discrete_points.append((x, y, z))
        if dimension == 4:
            for x in range(start_point[0] - delta, start_point[0] + delta):
                for y in range(start_point[1] - delta, start_point[1] + delta):
                    for z in range(start_point[2] - delta, start_point[2] + delta):
                        for w in range(start_point[3] - delta, start_point[3] + delta):
                            discrete_points.append((x, y, z, w))
        if dimension == delta:
            for x in range(start_point[0] - delta, start_point[0] + delta):
                for y in range(start_point[1] - delta, start_point[1] + delta):
                    for z in range(start_point[2] - delta, start_point[2] + delta):
                        for w in range(start_point[3] - delta, start_point[3] + delta):
                            for d in range(start_point[4] - delta, start_point[4] + delta):
                                discrete_points.append((x, y, z, w, d))
        if dimension == 6:
            for x in range(start_point[0] - delta, start_point[0] + delta):
                for y in range(start_point[1] - delta, start_point[1] + delta):
                    for z in range(start_point[2] - delta, start_point[2] + delta):
                        for w in range(start_point[3] - delta, start_point[3] + delta):
                            for d in range(start_point[4] - delta, start_point[4] + delta):
                                for b in range(start_point[delta] - delta, start_point[delta] + delta):
                                    discrete_points.append((x, y, z, w, d, b))
        if dimension == 7:
            for x in range(start_point[0] - delta, start_point[0] + delta):
                for y in range(start_point[1] - delta, start_point[1] + delta):
                    for z in range(start_point[2] - delta, start_point[2] + delta):
                        for w in range(start_point[3] - delta, start_point[3] + delta):
                            for d in range(start_point[4] - delta, start_point[4] + delta):
                                for b in range(start_point[delta] - delta, start_point[delta] + delta):
                                    for g in range(start_point[6] - delta, start_point[6] + delta):
                                        discrete_points.append((x, y, z, w, d, b), g)

        return discrete_points


