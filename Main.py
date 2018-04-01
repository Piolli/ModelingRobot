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
# cube = c.Rectangle(v.Vector3D(0, 0, 0), v.Vector3D(300, 300, 10))
# cube1 = c.Rectangle(v.Vector3D(0, 150, 0), v.Vector3D(100, 100, 5))
# divjok.add_to_draw(cube)
# divjok.add_to_draw(cube1)
for i in range(0, 1):
    # cube.rotate_y(1)
    # cube1.rotate_y(-1)
    divjok.clear_canvas()
    divjok.create_coordinate_axis()
    divjok.draw()
    divjok.update()

# --------REQUIRED TASK---------
conf_space = s.ConfigurationSpace(5, 1000, 1000)
conf_space.draw_bg_lines()
conf_space.draw_axis()
# conf_space.delta_window()
conf_space.manipulator_window()
obstacle_window = wo.ObstacleWindow(divjok, conf_space)


# obstacle_window.draw_obstacles_from_report_data()

# The method of full search for two targets
def full_search():
    obstacles = list()
    # Start point
    start_point = (90, 90)
    # Target
    target_point = (90, -90)

    conf_space.draw_point(90, 90, color="red")
    conf_space.draw_point(90, -90, color="red")

    open_tops = list(list(tuple()))
    close_tops = list(list(tuple()))
    open_tops.append([start_point])

    # List of paths to target top
    top_path = list()
    for i in range(0, 50000):
        if len(open_tops) != 0:
            close_tops.append(open_tops.pop(0))
        else:
            break
        one_top = close_tops.pop(0)
        next_points = conf_space.neighbours(one_top[len(one_top) - 1])

        # print(next_points)


        for next_point in next_points:
            conf_space.draw_point(next_point[0], next_point[1])
            if next_point not in obstacles:
                new_top = one_top.copy()
                new_top.append(next_point)
                open_tops.append(new_top)

        for next_point in next_points:
            if next_point not in obstacles:
                if next_point == target_point:
                    print("next", next_point)
                    one_top.append(target_point)
                    print("Finded! ", one_top)
                    top_path.append(one_top)

                    # break

                    # ------------------------------
                    # print(len(top_path))
                    # for index_path in range(len(top_path)):
                    #     path_points = top_path[index_path]
                    #     for i in range(0, len(path_points) - 1):
                    #         select_point = path_points[i]
                    #         next_point = path_points[i + 1]
                    #         conf_space.draw_intersection_line(v.Vector3D(select_point[0], select_point[1], 0),
                    #                                           v.Vector3D(next_point[0], next_point[1], 0))


def full_search2(q0, qT):
    def borders(point):
        Border = [-180, 180]
        for i in range(2):
            if (point[i] < Border[0]):
                return 0
            elif (point[i] > Border[1]):
                return 0
        return 1

    def check_point(point, array):
        if (point in array):
            return 1
        else:
            return 0

    def check_is_on_obstacle(q, lenght, obstacles) -> bool:
        lenght = 100
        # Pi, Pi1 = conf_space.manipulator(q[0], q[1], lenght)
        # P = [[Pi, Pi1], [v.Vector3D(0, 0, 0), Pi]]

        for obstacle in obstacles:
            for i in range(conf_space.n):
                t = 0
                point_i = conf_space.get_manipulator_position(i, q, lenght)
                point_i1 = conf_space.get_manipulator_position(i + 1, q, lenght)
                while t <= 1:
                    # Ai = [Pi1.x + (Pi.x - Pi1.x) * t,
                    #       Pi1.y + (Pi.y - Pi1.y) * t,
                    #       Pi1.z + (Pi.z - Pi1.z) * t
                    #       ]
                    #
                    # translateAi = [Ai[0] - obstacle[0],
                    #                Ai[1] - obstacle[1],
                    #                Ai[2] - obstacle[2]]
                    #

                    x = point_i1[0][0] + (point_i[0][0] - point_i1[0][0])*t
                    y = point_i1[1][0] + (point_i[1][0] - point_i1[1][0])*t
                    z = point_i1[2][0] + (point_i[2][0] - point_i1[2][0])*t

                    if (obstacle[0] <= x <= obstacle[3]) and\
                       (obstacle[1] <= y <= obstacle[4]) and\
                       (obstacle[2] <= z <= obstacle[5]):
                        return True

                    t = round(t + 0.01, 2)

        return False

    opened = [q0]
    closed = []
    id = 0
    temporary_point = q0[:]
    temporary_point.append(id)
    path_temp = [temporary_point]
    path = []
    pathPoints = []
    q0test = 0
    changePathK = 0
    zaprAdd = []
    zaprMass = []
    publicPath = []
    q0temp = q0
    zaprPoints = []
    failtest = 0
    obstacles = obstacle_window.get_array_default_obstacles()
    prcol = len(obstacles)
    # obstacles = []
    # Full search

    for i in range(len(zaprPoints)):
        conf_space.canvas.delete(zaprPoints[i])

    while check_point(qT, opened) == 0:
        if (len(opened) == 0):
            failtest = 1
            print("failtest", failtest)
            break
        Near = conf_space.neighbours(opened[0])
        closed.append(opened[0])
        for i in range(len(Near)):
            if ((check_point(Near[i], opened) == 0)
                and (check_point(Near[i], closed) == 0)
                and (borders(Near[i]) == 1)
                and (check_point(Near[i], zaprMass) == 0)
                # and not (check_is_on_obstacle(Near[i], 90, obstacles))
                ):
                    opened.append(Near[i])
                    temporary_point = Near[i][:]
                    temporary_point.append(id)
                    path_temp.append(temporary_point)

        del opened[0]
        id += 1

    print("path", path_temp)
    print("id", id)

    id = len(path_temp) - 1

    # For create path
    while (id != 0):
        temporary_point = path_temp[id][:]
        del temporary_point[-1]
        path.append(temporary_point)
        id = path_temp[id][conf_space.n]

    if (failtest == 0):
        path.append(q0)
        path.reverse()
        print("path", path)
        # conf_space.draw_path(path)
        if (q0test == 0):
            q0test = 1
            changePathK = changePathK + 1
            print("len path", len(path))
            for i in range(1, len(path) - 1):
                pathPoints.append([])
                pathPoints[i - 1] = conf_space.draw_point(path[i][0], path[i][1])
        if (len(zaprMass) != 0):
            print('q(%i): %s' % (changePathK, path[0]))
            print('ZAPR(%i): %s' % (changePathK, zaprMass))
            print('PATH(%i): %s' % (changePathK, path))
            tempoval0 = conf_space.draw_point(q0temp[0], q0temp[1], color="orange")  # Отображение начальной точки
            changePathK = changePathK + 1
            if (1 == 1):
                for i in range(len(pathPoints)):
                    conf_space.canvas.delete(pathPoints[i])
                pathPoints = []
                for i in range(1, len(publicPath) - 1):
                    pathPoints.append([])
                    pathPoints[i - 1] = conf_space.draw_point(publicPath[i][0], publicPath[i][1], color="light blue")
                temp = len(pathPoints)
                pathPoints.append([])
                pathPoints[len(pathPoints) - 1] = conf_space.draw_point(path[0][0], path[0][1], color="lawn green")

                for i in range(1, len(path) - 1):
                    pathPoints.append([])
                    pathPoints[temp + i - 1] = conf_space.draw_point(path[i][0], path[i][1], color="light blue") # Отображение начальной точки
                for i in range(len(zaprPoints)):
                    conf_space.canvas.delete(zaprPoints[i])
                zaprPoints = []
                for i in range(len(zaprMass)):
                    zaprPoints.append([])
                    zaprPoints[i] = conf_space.draw_point(zaprMass[i][0], zaprMass[i][1], color="red")

                print("Pause", 'Точка смены пути q%i: %s (Выделена зеленым)\nPress OK' % (changePathK - 1, publicPath[len(publicPath) - 1]))
        if (prcol != 0):
            for i in range(len(path)):
                if (check_is_on_obstacle(path[i], 100, obstacles)):
                    zaprMass.append(path[i])
                    sos_temp = conf_space.neighbours(path[i])
                    for i in range(len(sos_temp)):
                        if check_is_on_obstacle(sos_temp[i], 100, obstacles) and check_point(sos_temp[i], zaprMass) == 0:
                            zaprAdd.append(sos_temp[i])
                    full_search2(publicPath[len(publicPath) - 1], qT)
                    return 0
                else:
                    if (check_point(path[i], publicPath) == 0):
                        publicPath.append(path[i])
            publicPath.append(qT)

            for i in range(len(pathPoints)):
                conf_space.canvas.delete(pathPoints[i])
            pathPoints = []
            for i in range(len(zaprPoints)):
                conf_space.canvas.delete(zaprPoints[i])
            zaprPoints = []

            for i in range(1, len(publicPath) - 2):
                pathPoints.append([])
                pathPoints[i - 1] = conf_space.draw_point(path[i][0], path[i][1], color="light blue")

            for i in range(len(zaprMass)):
                zaprPoints.append([])
                zaprPoints[i] = conf_space.draw_point(path[i][0], path[i][1], color="red")  # Отображение начальной точки
        print("Success")
        print("Pause", 'Цель достигнута, путь в файле\nPress OK')

# full_search()

q0 = [90, 90]
qT = [-90, 90]

# full_search2(q0, qT)
# fs.FullSearch(q0, qT, obstacle_window, conf_space).full_search(q0, qT)
fs.FullSearch(q0, qT, obstacle_window, conf_space).my_full_search(q0, qT)
# p11, p12 = conf_space.manipulator(q0[0], q0[1], 90)
# conf_space.draw_point(p11.x, p11.y, color='red')
# conf_space.draw_point(p12.x, p12.y, color='red')

# p21, p22 = conf_space.manipulator(qT[0], qT[1], 90)
# conf_space.draw_point(p21.x, p21.y, color='red')
# conf_space.draw_point(p22.x, p22.y, color='red')

obstacle_window.draw_obstacles_from_report_data()

conf_space.draw_point(q0[0], q0[1])
conf_space.draw_point(qT[0], qT[1])

divjok.loop()
