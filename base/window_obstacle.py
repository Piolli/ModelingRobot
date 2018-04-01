from tkinter import *
import base.Vector3D as v
import base.models.mcube as c
import base.logix as d
import base.configuration_space as s


class ObstacleWindow:
    def __init__(self, divjok: d.Divjok, conf_space: s.ConfigurationSpace) -> None:
        self.conf_space = conf_space
        self.divjok = divjok
        top = Toplevel()
        top.deiconify()
        top.title("Add rectangle")

        Label(top, text="Enter x1").grid(row=0, column=0)
        Label(top, text="Enter y1").grid(row=0, column=1)
        Label(top, text="Enter z1").grid(row=0, column=2)

        self.rect_x1 = Entry(top)
        self.rect_y1 = Entry(top)
        self.rect_z1 = Entry(top)
        self.rect_x1.grid(row=1, column=0)
        self.rect_y1.grid(row=1, column=1)
        self.rect_z1.grid(row=1, column=2)

        Label(top, text="Enter x6").grid(row=2, column=0)
        Label(top, text="Enter y6").grid(row=2, column=1)
        Label(top, text="Enter z6").grid(row=2, column=2)

        self.rect_x2 = Entry(top)
        self.rect_y2 = Entry(top)
        self.rect_z2 = Entry(top)
        self.rect_x2.grid(row=3, column=0)
        self.rect_y2.grid(row=3, column=1)
        self.rect_z2.grid(row=3, column=2)

        Button(top, text="Enter", width=15, command=self.callback).grid(row=4, column=1)

    def callback(self):
        x1 = int(self.rect_x1.get())
        y1 = int(self.rect_y1.get())
        z1 = int(self.rect_z1.get())

        x2 = int(self.rect_x2.get())
        y2 = int(self.rect_y2.get())
        z2 = int(self.rect_z2.get())

        v1 = v.Vector3D(x1, y1, z1)
        v2 = v.Vector3D(x2, y2, z2)
        cube3 = c.Rectangle(v1, v2)
        # TODO Delete conf_space if error show cube
        self.divjok.add_to_draw(cube3)
        self.divjok.draw()
        # self.conf_space.draw_rectangle(v1, v2)

    def draw_obstacle(self, x0, y0, z0, x1, y1, z1):
        v1 = v.Vector3D(x0, y0, z0)
        v2 = v.Vector3D(x1, y1, z1)
        cube3 = c.Rectangle(v1, v2)

        self.divjok.add_to_draw(cube3)
        self.divjok.draw()

    def draw_obstacles_from_report_data(self):
        # Find path
        # self.draw_obstacle(-500,  24,   140,  500,   56,  180)
        # self.draw_obstacle( 60,  -340, -200,  500,  -60,  200)
        # self.draw_obstacle(-500, -340, -400, -140,  -60,  400)
        # self.draw_obstacle(-500, -500, -6,    500,  500,  -2)
        # self.draw_obstacle(-140,  140, -400, -100,  180,  400)

        # Not find path
        self.draw_obstacle(-500,  -56,   80,  500,   -24,  120)
        self.draw_obstacle( 60,  -340, -200,  500,  -60,  200)
        self.draw_obstacle(-500, -340, -400, -140,  -60,  400)
        self.draw_obstacle(-500, -500, -6,    500,  500,  -2)
        self.draw_obstacle(-140,  140, -400, -100,  180,  400)

    def get_array_default_obstacles(self):
        obstacles = []

        # Find path
        # obstacles.append((-500,  24,   140,  500,   56,  180))
        # obstacles.append(( 60,  -340, -200,  500,  -60,  200))
        # obstacles.append((-500, -340, -400, -140,  -60,  400))
        # obstacles.append((-500, -500, -6,    500,  500,  -2))
        # obstacles.append((-140,  140, -400, -100,  180,  400))

        # Not find path
        obstacles.append((-500,  -56,   80,  500,   -24,  120))
        obstacles.append(( 60,  -340, -200,  500,  -60,  200))
        obstacles.append((-500, -340, -400, -140,  -60,  400))
        obstacles.append((-500, -500, -6,    500,  500,  -2))
        obstacles.append((-140,  140, -400, -100,  180,  400))

        return obstacles