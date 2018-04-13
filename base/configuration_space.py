from tkinter import *
import base.Vector3D as v
import math as m
import base.logix as l
import operator
import base.matrixutils as utils


class ConfigurationSpace:
    def __init__(self, delta: int, width, height) -> None:
        self.__width = width
        self.__height = height
        self.__delta = delta

        self.__X0 = width / 2
        self.__Y0 = height / 2

        # Space dimension
        self.n = 2

        # For full search
        self.q0 = []
        self.qT = []

        self.top = Toplevel()
        self.top.deiconify()
        self.top.title("Configuration space")
        self.top.geometry("{0}x{1}".format(self.__width, self.__height))
        self.canvas = Canvas(self.top, width=self.__width, height=self.__height, bg="white")
        self.canvas.pack()

    def draw_bg_lines(self):
        delta = self.__delta * self.__X0 / 180
        count_of_cells = int(self.__height / delta / 2)
        for i in range(0, count_of_cells):
            # Y axis
            self.canvas.create_line(self.__X0 + delta, 0, self.__X0 + delta, self.__height)
            self.canvas.create_line(self.__X0 - delta, 0, self.__X0 - delta, self.__height)

            # X axis
            self.canvas.create_line(0, self.__Y0 + delta, self.__width, self.__Y0 + delta)
            self.canvas.create_line(0, self.__Y0 - delta, self.__width, self.__Y0 - delta)

            delta += self.__delta * self.__X0 / 180

    def draw_axis(self):
        self.canvas.create_line(0, self.__Y0, self.__width, self.__Y0, arrow='last', fill="red", width=3)
        self.canvas.create_line(self.__X0, self.__height, self.__X0, 0, arrow='last', fill="red", width=3)

    def redraw(self):
        self.canvas.delete("all")
        self.draw_axis()
        self.draw_bg_lines()

    def get_delta_frame(self, master):
        top = Frame(master)
        # top.deiconify()
        # top.title("Set delta")

        Label(top, text="delta: ").grid(row=0, column=0)
        self.__delta_entry = Entry(top)
        self.__delta_entry.grid(row=0, column=1)

        Button(top, text="Set delta", command=self.delta_callback).grid(row=1, column=1)

        return top

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
        return self.canvas.create_oval(x - size + self.__X0, self.__Y0 - (y - size), x + size + self.__X0,
                                       self.__Y0 - (y + size), width=0, fill=color)
        # print(x - size + self.__X0, self.__Y0 - (y - size), x + size + self.__X0, self.__Y0 - (y + size))

    def draw_point_tuple(self, point, color):
        self.draw_point(point[0], point[1], color=color)

    def draw_line(self, vector1: v.Vector3D, vector2: v.Vector3D):
        mult_coef_x = self.__X0 / 180
        mult_coef_y = self.__Y0 / 180

        vector1.x *= mult_coef_x
        vector1.y *= mult_coef_y

        vector2.x *= mult_coef_x
        vector2.y *= mult_coef_y

        self.canvas.create_line(vector1.x + self.__X0, self.__Y0 - vector1.y, self.__X0 + vector2.x,
                                self.__Y0 - vector2.y, width=2)

    def draw_line_for_manipulator(self, vector1: v.Vector3D, vector2: v.Vector3D):
        mult_coef_x = self.__X0 / 180
        mult_coef_y = self.__Y0 / 180

        # vector1.x *= mult_coef_x
        # vector1.y *= mult_coef_y

        vector2.x *= mult_coef_x
        vector2.y *= mult_coef_y

        self.canvas.create_line(vector1.x + self.__X0, self.__Y0 - vector1.y, self.__X0 + vector2.x,
                                self.__Y0 - vector2.y, width=3, fill="blue", arrow="last")

    def draw_intersection_line(self, vector1: v.Vector3D, vector2: v.Vector3D):
        coef = self.__delta * 180 / self.__width * 2
        vector1.x *= coef
        vector1.y *= coef

        vector2.x *= coef
        vector2.y *= coef
        self.draw_line(vector1, vector2)

    def manipulator(self, a1: int, a2: int, L: int):
        L = 100
        Q1 = m.radians(a1)
        Q2 = m.radians(a2)

        # First vector from (0, 0)
        vA = v.Vector3D(0, 0, 0)
        vA.x = round(L * m.cos(Q1), 2)
        vA.y = round(L * m.sin(Q1), 2)

        # Second vector from end vA
        vS = v.Vector3D(0, 0, 0)
        vS.x = round(L * -m.cos(Q1 + Q2) + vA.x, 2)
        vS.y = round(L * m.sin(Q1 + Q2) + vA.y, 2)

        return vA, vS

    def get_manipulator_position(self, i, q, length):
        if i == 0 or i == 1:
            return [[0], [0], [length if i == 1 else 0], [0]]

        if i == 2:
            a = utils.matrixmult(utils.matrixmult(self.transition_matrix(q[0], length, 0, 270),
                                      self.transition_matrix(q[1], 0, 0, 90)), [[0], [0], [length], [1]])
            return a
        elif i > 2:
            temp = utils.matrixmult(self.transition_matrix(q[0], length, 0, 270),
                              self.transition_matrix(q[1], 0, 0, 90))
            for j in range(1, i - 1):
                if j % 2 == 0:
                    temp = utils.matrixmult(temp, self.transition_matrix(q[j + 1], 0, 0, 90))
                else:
                    temp = utils.matrixmult(temp, self.transition_matrix(q[j + 1], 2 * length, 0, 270))
            if i % 2 == 0:
                temp = utils.matrixmult(temp, [[0], [0], [length], [1]])
            else:
                temp = utils.matrixmult(temp, [[0], [0], [0], [1]])
            return temp

    def transition_matrix(self, omega, s, a, alpha):
        tempM = [[round(m.cos(m.radians(omega)), 6),
                  -round(m.sin(m.radians(omega)), 6) * round(m.cos(m.radians(alpha)), 6),
                  round(m.sin(m.radians(omega)), 6) * round(m.sin(m.radians(alpha)), 6),
                  a * round(m.cos(m.radians(omega)), 6)],
                 [round(m.sin(m.radians(omega)), 6),
                  round(m.cos(m.radians(omega)), 6) * round(m.cos(m.radians(alpha)), 6),
                  -round(m.cos(m.radians(omega)), 6) * round(m.sin(m.radians(alpha)), 6),
                  a * round(m.sin(m.radians(omega)), 6)],
                 [0, m.sin(m.radians(alpha)), round(m.cos(m.radians(alpha)), 6), s],
                 [0, 0, 0, 1]
                 ]
        return tempM

    def get_manipulator_frame(self, master):

        top = Frame(master)
        # top.deiconify()
        # top.title("Add manipulator")

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
                self.q0 = [int(q0_list[0].get()), int(q0_list[1].get())]
                self.qT = [int(qt_list[0].get()), int(qt_list[1].get())]

                self.draw_point(self.q0[0], self.q0[1], color="green")
                self.draw_point(self.qT[0], self.qT[1], color="yellow")


        Button(top, text="Set n", command=set_n_callback).grid(row=0, column=2)
        Button(top, text="Draw", command=draw_callback).grid(row=0, column=3)

        return top

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

        self.canvas.create_rectangle(vector1.x + self.__X0, self.__Y0 - vector1.y, self.__X0 + vector2.x,
                                     self.__Y0 - vector2.y, width=3, fill="red")

    def draw_intersection_cell(self, cell_x, cell_y, color="red"):
        coef = self.__delta * 180 / self.__height * 2
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
                                        discrete_points.append((x, y, z, w, d, b, g))

        return discrete_points

    # For find path
    def is_forbidden_point(self, point, obstacles):
        for obstacle in obstacles:
            for i in range(len(obstacle)):
                if point[i] >= obstacle[i] and point[i] <= obstacle[i]:
                    return False

        return True

    # Create path of q0 to qt
    def create_path(self, q0, qt):
        pass

    def draw_q(self, q):
        self.draw_point(q[0], q[1])

    # Check q of bounds of conf space
    def bounds(self, q):
        for i in range(self.n):
            if -180 > q[i] > 180:
                return False
        return True

    # Get full array of values for multiply with q
    def get_TT(self):
        TT = []
        zeropoint = []
        tempTT = []
        mul = [-1, 0, 1]
        TT = []
        for i in range(3 ** self.n):
            for j in range(self.n):
                k = i // (3 ** j) - i // (3 ** (j + 1)) * 3
                tempTT.append(mul[k])
            TT.append(tempTT)
            tempTT = []

        for j in range(self.n):
            zeropoint.append(0)

        zeropoint = [zeropoint]

        for i in range(3 ** self.n - 1):
            if TT[i] in zeropoint:
                del TT[i]
                break

        return TT

    def draw_path(self, path_array, color="blue"):
        draw_points = []
        for point in path_array:
            draw_points.append(self.draw_point(point[0], point[1], color=color))

        return draw_points

    # Get all neighbours with help get_TT
    def neighbours(self, qc):
        n = self.n
        qTemp = [0 for i in range(n)]
        TT = self.get_TT()
        tempS = []

        for i in range(3 ** n - 1):
            for j in range(n):
                qTemp[j] = qc[j] + TT[i][j]*self.__delta
            tempS.append(qTemp)
            qTemp = [0 for i in range(n)]

        # ------------------
        # Sort by distance
        # mapPointToDistance = {}
        #
        # def distance(point1: (), point2: ()):
        #     dist = 0
        #     for i in range(len(point1)):
        #         dist += (point2[i] - point1[i]) ** 2
        #     return round(m.sqrt(dist), 3)
        #
        # for point in tempS:
        #     mapPointToDistance[tuple(point)] = distance(point, qc)
        #
        # sorted_x = sorted(mapPointToDistance.items(), key=operator.itemgetter(1))

        # result_points = list()
        # for i in range(3**n - 1):
        #     if sorted_x[i][0] != qc:
        #         result_points.append(sorted_x[i][0])
        # -------------------
        # print(tempS)
        return tempS
        # return result_points
