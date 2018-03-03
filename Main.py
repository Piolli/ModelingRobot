import base.logix as d
import base.models.mcube as c
import base.Vector3D as v
import base.configuration_space as s
import base.window_obstacle as wo
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
conf_space = s.ConfigurationSpace(50, 800, 800)
conf_space.draw_bg_lines()
conf_space.draw_axis()
conf_space.delta_window()
conf_space.manipulator_window()
wo.ObstacleWindow(divjok, conf_space)
obstacles = list()

# Start
start_point = (1, 1)
conf_space.draw_intersection_cell(start_point[0], start_point[1], color="blue")

# Obstacles
conf_space.draw_intersection_cell(3, 1)
conf_space.draw_intersection_cell(3, 2)
conf_space.draw_intersection_cell(1, 2)
obstacles.append((3, 1))
obstacles.append((3, 2))
obstacles.append((1, 2))
obstacles.append((1, 2))


# Target
target_point = (4, 3)
conf_space.draw_intersection_cell(target_point[0], target_point[1], "black")

# Draw horizontal lines
for i in range(6):
    conf_space.draw_intersection_cell(i, 0, color="darkgreen")
    conf_space.draw_intersection_cell(i, 4, color="darkgreen")
    obstacles.append((i, 0))
    obstacles.append((i, 4))

# Draw vertical lines
for i in range(5):
    conf_space.draw_intersection_cell(0, i, color="darkgreen")
    conf_space.draw_intersection_cell(5, i, color="darkgreen")
    obstacles.append((0, i))
    obstacles.append((5, i))

open_tops = list(list(tuple()))
close_tops = list(list(tuple()))
open_tops.append([start_point])

is_find_right_top = False
is_find_top_right_top = False
is_find_top_left_top = False
# List of paths to target top
top_path = list()
for i in range(0, 10):
    if len(open_tops) != 0:
        close_tops.append(open_tops.pop(0))
    else:
        break
    one_top = close_tops.pop(0)
    next_points = conf_space.find_next_points(one_top[len(one_top) - 1])

    for next_point in next_points:
        if next_point not in obstacles:
            new_top = one_top.copy()
            new_top.append(next_point)
            open_tops.append(new_top)

    for next_point in next_points:
        if next_point not in obstacles:
            if next_point == target_point:
                one_top.append(target_point)
                print("Finded! ", one_top)
                top_path.append(one_top)

                # break

# ------------------------------
print(len(top_path))
for index_path in range(len(top_path)):
    path_points = top_path[index_path]
    for i in range(0, len(path_points) - 1):
        select_point = path_points[i]
        next_point = path_points[i + 1]
        conf_space.draw_intersection_line(v.Vector3D(select_point[0], select_point[1], 0),
                                          v.Vector3D(next_point[0], next_point[1], 0))
divjok.loop()
