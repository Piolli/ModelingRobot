from tkinter import *
import base.Vector3D as v
import base.models.mcube as c
import base.logix as d
import base.configuration_space as s


class ObstacleWindow:
    def __init__(self, divjok: d.Divjok, conf_space: s.ConfigurationSpace, master) -> None:
        self.conf_space = conf_space
        self.divjok = divjok
        self.frame = Frame(master)
        # self.frame.deiconify()
        # self.frame.title("Add rectangle")

        Label(self.frame, text="Enter x1").grid(row=0, column=0)
        Label(self.frame, text="Enter y1").grid(row=0, column=1)
        Label(self.frame, text="Enter z1").grid(row=0, column=2)

        self.rect_x1 = Entry(self.frame)
        self.rect_y1 = Entry(self.frame)
        self.rect_z1 = Entry(self.frame)
        self.rect_x1.grid(row=1, column=0)
        self.rect_y1.grid(row=1, column=1)
        self.rect_z1.grid(row=1, column=2)

        Label(self.frame, text="Enter x6").grid(row=2, column=0)
        Label(self.frame, text="Enter y6").grid(row=2, column=1)
        Label(self.frame, text="Enter z6").grid(row=2, column=2)

        self.rect_x2 = Entry(self.frame)
        self.rect_y2 = Entry(self.frame)
        self.rect_z2 = Entry(self.frame)
        self.rect_x2.grid(row=3, column=0)
        self.rect_y2.grid(row=3, column=1)
        self.rect_z2.grid(row=3, column=2)

        self.obstacles = self.get_array_default_obstacles()

        Button(self.frame, text="Enter", width=15, command=self.callback).grid(row=4, column=1)

    def get_obstacles_frame(self):
        return self.frame

    def callback(self):
        x1 = int(self.rect_x1.get())
        y1 = int(self.rect_y1.get())
        z1 = int(self.rect_z1.get())

        x2 = int(self.rect_x2.get())
        y2 = int(self.rect_y2.get())
        z2 = int(self.rect_z2.get())

        self.obstacles.append((x1, y1, z1, x2, y2, z2))

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
        obstacles = self.get_array_default_obstacles()

        for obstacle in obstacles:
            self.draw_obstacle(obstacle[0], obstacle[1], obstacle[2],
                               obstacle[3], obstacle[4], obstacle[5])


        # Not find path
        # self.draw_obstacle(-500,  -56,   80,  500,   -24,  120)
        # self.draw_obstacle( 60,  -340, -200,  500,  -60,  200)
        # self.draw_obstacle(-500, -340, -400, -140,  -60,  400)
        # self.draw_obstacle(-500, -500, -6,    500,  500,  -2)
        # self.draw_obstacle(-140,  140, -400, -100,  180,  400)

    def get_array_default_obstacles(self):
        obstacles = []

        # Find path
        obstacles.append((-500,  24,   140,  500,   56,  180))
        obstacles.append(( 60,  -340, -200,  500,  -60,  200))
        obstacles.append((-500, -340, -400, -140,  -60,  400))
        obstacles.append((-500, -500, -6,    500,  500,  -2))
        obstacles.append((-140,  140, -400, -100,  180,  400))
        #
        # Not find path
        # obstacles.append((-500,  -56,   80,  500,   -24,  120))
        # obstacles.append(( 60,  -340, -200,  500,  -60,  200))
        # obstacles.append((-500, -340, -400, -140,  -60,  400))
        # obstacles.append((-500, -500, -6,    500,  500,  -2))
        # obstacles.append((-140,  140, -400, -100,  180,  400))

        return obstacles