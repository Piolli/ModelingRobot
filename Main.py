import base.logix as d
import base.models.mcube as c
import base.Vector3D as v
import base.configuration_space as s
import base.window_obstacle as wo
from tkinter import *
import base.full_search as fs
import time as t

# Increment recursion deep
import sys

sys.setrecursionlimit(1000000000)

divjok = d.Divjok()

# --------REQUIRED TASK---------
conf_space = s.ConfigurationSpace(5, 1000, 1000, divjok)
conf_space.draw_bg_lines()
conf_space.draw_axis()

radio_buttons_value = IntVar()


divjok.create_coordinate_axis()

main_menu = Toplevel()
main_menu.title = "Main menu"
# Frames
obstacle_window = wo.ObstacleWindow(divjok, conf_space, main_menu)
obstacle_frame = obstacle_window.get_obstacles_frame()
delta_frame = conf_space.get_delta_frame(main_menu)
manipulator_frame = conf_space.get_manipulator_frame(main_menu)

delta_frame.grid(row=0, column=0)
Label(main_menu, text="------------------------------------------------------------------------").grid(row=1, column=0)
manipulator_frame.grid(row=2, column=0)
Label(main_menu, text="------------------------------------------------------------------------").grid(row=3, column=0)
obstacle_frame.grid(row=4, column=0)
Label(main_menu, text="------------------------------------------------------------------------").grid(row=5, column=0)


def step_by_step_path_callback():
    obstacle_window.type_of_using_obstacles = radio_buttons_value.get()
    fs.FullSearch(obstacle_window.get_array_default_obstacles(), conf_space, True)

def simple_path_callback():
    obstacle_window.type_of_using_obstacles = radio_buttons_value.get()
    fs.FullSearch(obstacle_window.get_array_default_obstacles(), conf_space, False)


step_by_step_path_button = Button(main_menu, text="Find path step by step", command=step_by_step_path_callback)
step_by_step_path_button.grid(row=6, column=0)

simple_path_button = Button(main_menu, text="Find path", command=simple_path_callback)
simple_path_button.grid(row=7, column=0)


default_radio_button = Radiobutton(main_menu, text="Достижимость", variable=radio_buttons_value, value=2)
default_radio_button.grid(row=8, column=0)
default_radio_button.select()

Radiobutton(main_menu, text="Недостижимость", variable=radio_buttons_value, value=1).grid(row=9)

obstacle_window.draw_obstacles_from_report_data()

divjok.loop()
