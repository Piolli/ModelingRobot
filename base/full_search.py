import base.Vector3D as v


class FullSearch:
    def __init__(self, q0, qT, obstacle_window, conf_space):
        self.q0 = q0
        self.qT = qT
        self.conf_space = conf_space
        self.pathPoints = []
        self.q0test = 0
        self.changePathK = 0
        self.zaprAdd = []
        self.zaprMass = []
        self.publicPath = []
        self.q0temp = q0
        self.zaprPoints = []
        self.failtest = 0
        self.obstacles = obstacle_window.get_array_default_obstacles()
        self.prcol = len(self.obstacles)

        self.forbidden_points = []
        self.change_path_points = []
        self.complete_path = [q0]
        self.count_change_path = 0
        self.complete_path_is_finded = False
        self.is_show_data_path = False

    def full_search(self, q0, qT):

        id = 0
        temporary_point = q0[:]
        temporary_point.append(id)

        print("temp", temporary_point)

        opened = [q0]
        closed = []
        path_temp = [temporary_point]
        path = []

        for i in range(len(self.zaprPoints)):
            self.conf_space.canvas.delete(self.zaprPoints[i])

        while self.check_point(qT, opened) == 0:
            if (len(opened) == 0):
                failtest = 1
                print("failtest", failtest)
                break
            Near = self.conf_space.neighbours(opened[0])
            closed.append(opened[0])
            for i in range(len(Near)):
                if ((self.check_point(Near[i], opened) == 0)
                    and (self.check_point(Near[i], closed) == 0)
                    and (self.borders(Near[i]) == 1)
                    and (self.check_point(Near[i], self.zaprMass) == 0)
                    # and not (self.check_is_on_obstacle(Near[i], 100, self.obstacles))
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
            id = path_temp[id][self.conf_space.n]

        if (self.failtest == 0):
            path.append(q0)
            path.reverse()
            print("path", path)
            # conf_space.draw_path(path)
            if (self.q0test == 0):
                q0test = 1
                self.changePathK = self.changePathK + 1
                print("len path", len(path))
                for i in range(1, len(path) - 1):
                    self.pathPoints.append([])
                    self.pathPoints[i - 1] = self.conf_space.draw_point(path[i][0], path[i][1], color="light blue")
            if (len(self.zaprMass) != 0):
                print('q(%i): %s' % (self.changePathK, path[0]))
                print('ZAPR(%i): %s' % (self.changePathK, self.zaprMass))
                print('PATH(%i): %s' % (self.changePathK, path))
                tempoval0 = self.conf_space.draw_point(self.q0temp[0], self.q0temp[1],
                                                       color="orange")  # Отображение начальной точки
                self.changePathK = self.changePathK + 1
                if (1 == 1):
                    # for i in range(len(self.pathPoints)):
                    #     self.conf_space.canvas.delete(self.pathPoints[i])
                    pathPoints = []
                    for i in range(1, len(self.publicPath) - 1):
                        pathPoints.append([])
                        pathPoints[i - 1] = self.conf_space.draw_point(self.publicPath[i][0], self.publicPath[i][1],
                                                                       color="light blue")
                    temp = len(pathPoints)
                    pathPoints.append([])
                    pathPoints[len(pathPoints) - 1] = self.conf_space.draw_point(path[0][0], path[0][1],
                                                                                 color="lawn green")

                    for i in range(1, len(path) - 1):
                        pathPoints.append([])
                        pathPoints[temp + i - 1] = self.conf_space.draw_point(path[i][0], path[i][1],
                                                                              color="light blue")  # Отображение начальной точки
                    # for i in range(len(self.zaprPoints)):
                    #     self.conf_space.canvas.delete(self.zaprPoints[i])
                    zaprPoints = []
                    for i in range(len(self.zaprMass)):
                        zaprPoints.append([])
                        zaprPoints[i] = self.conf_space.draw_point(self.zaprMass[i][0], self.zaprMass[i][1],
                                                                   color="red")

                    print("Pause", 'Точка смены пути q%i: %s (Выделена зеленым)\nPress OK' % (
                        self.changePathK - 1, self.publicPath[len(self.publicPath) - 1]))
            if (self.prcol != 0):
                for i in range(len(path)):
                    if (self.check_is_on_obstacle(path[i], 100, self.obstacles)):
                        self.zaprMass.append(path[i])
                        sos_temp = self.conf_space.neighbours(path[i])
                        for i in range(len(sos_temp)):
                            if self.check_is_on_obstacle(sos_temp[i], 100, self.obstacles) and self.check_point(
                                    sos_temp[i],
                                    self.zaprMass) == 0:
                                self.zaprAdd.append(sos_temp[i])
                        self.full_search(self.publicPath[len(self.publicPath) - 1], qT)
                        return 0
                    else:
                        if (self.check_point(path[i], self.publicPath) == 0):
                            self.publicPath.append(path[i])
                self.publicPath.append(qT)

                # for i in range(len(self.pathPoints)):
                #     self.conf_space.canvas.delete(self.pathPoints[i])

                pathPoints = []

                # for i in range(len(self.zaprPoints)):
                #     self.conf_space.canvas.delete(self.zaprPoints[i])

                zaprPoints = []

                for i in range(1, len(self.publicPath) - 2):
                    pathPoints.append([])
                    pathPoints[i - 1] = self.conf_space.draw_point(self.publicPath[i][0], self.publicPath[i][1],
                                                                   color="light blue")

                for i in range(len(self.zaprMass)):
                    zaprPoints.append([])
                    zaprPoints[i] = self.conf_space.draw_point(self.zaprMass[i][0], self.zaprMass[i][1],
                                                               color="red")  # Отображение начальной точки
            print("Success")
            print("Pause", 'Цель достигнута, путь в файле\nPress OK')

    def my_full_search(self, q0, qT):
        if self.complete_path_is_finded:
            return
        opened = [q0]
        closed = []
        # Complete path for this iteration
        full_search_path = []
        # Mark the top
        id = 0
        # For full search create path
        temp_point = q0[:]
        temp_point.append(id)

        temp_path = [temp_point]

        # Full search for create path
        while qT not in opened:
            if len(opened) == 0:
                print("Путь не может быть найден")
                self.complete_path_is_finded = False
                self.is_show_data_path = True
                break

            # Get first top and delete from opened list
            first_top = opened.pop(0)
            closed.append(first_top)
            neighbours = self.conf_space.neighbours(first_top)

            # Check neighbours allowed tops
            for neighbour in neighbours:
                if self.check_neighbour(neighbour, opened, closed):
                    opened.append(neighbour)
                    temp_point = neighbour[:]
                    temp_point.append(id)
                    temp_path.append(temp_point)
            id += 1

        # Create path by last id
        id = len(temp_path) - 1
        while id != 0:
            temp_point = temp_path[id][:]
            # Delete id from top
            del temp_point[-1]
            full_search_path.append(temp_point)
            id = temp_path[id][self.conf_space.n]

        full_search_path.append(q0)
        full_search_path.reverse()
        # self.conf_space.draw_path(full_search_path)

        if not self.complete_path_is_finded:
            for i in range(len(full_search_path)):
                point = full_search_path[i]
                if self.check_is_on_obstacle(point, 100, self.obstacles) and not self.is_show_data_path:
                    previous_point = full_search_path[i - 1]
                    self.forbidden_points.append(point)
                    print("Ранее неизвестная запрещенная точка:", point)
                    self.change_path_points.append(previous_point)
                    print("Возвращаемся в предыдущую точку (точка смены пути) и начинаем сначала:", previous_point)
                    print("----------------")
                    self.my_full_search(previous_point, qT)
                    return 0
                else:
                    # Adding previous point to complete_path
                    self.complete_path.append(point)

        self.is_show_data_path = True

        self.conf_space.draw_path(self.change_path_points, color="darkgreen")
        self.conf_space.draw_path(self.forbidden_points, color="red")

        self.complete_path.append(qT)
        self.conf_space.draw_path(self.complete_path)

        if self.complete_path_is_finded and not self.is_show_data_path:
            print("Путь найден:", full_search_path)
        elif not self.is_show_data_path:
            print("Путь не найден")



        return 0

    def check_neighbour(self, neighbour, opened, closed):
        if (neighbour not in opened
            and neighbour not in closed
            and self.is_on_bounds(neighbour)
            and neighbour not in self.forbidden_points):
            return True

        return False

    def is_on_bounds(self, point):
        border = [-180, 180]
        for i in range(2):
            if point[i] < border[0] or point[i] > border[1]:
                return False
        return True

    def borders(self, point):
        Border = [-180, 180]
        for i in range(2):
            if (point[i] < Border[0]):
                return 0
            elif (point[i] > Border[1]):
                return 0
        return 1

    def check_point(self, point, array):
        if (point in array):
            return 1
        else:
            return 0

    def check_is_on_obstacle(self, q, lenght, obstacles) -> bool:
        if len(obstacles) == 0:
            return False
        lenght = 100
        Pi, Pi1 = self.conf_space.manipulator(q[0], q[1], lenght)
        P = [[Pi, Pi1], [v.Vector3D(0, 0, 0), Pi]]

        for obstacle in obstacles:
            for i in range(self.conf_space.n):
                t = 0
                point_i = self.conf_space.get_manipulator_position(i, q, lenght)
                point_i1 = self.conf_space.get_manipulator_position(i + 1, q, lenght)
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

                    x = point_i1[0][0] + (point_i[0][0] - point_i1[0][0]) * t
                    y = point_i1[1][0] + (point_i[1][0] - point_i1[1][0]) * t
                    z = point_i1[2][0] + (point_i[2][0] - point_i1[2][0]) * t

                    if (obstacle[0] <= x <= obstacle[3]) and \
                            (obstacle[1] <= y <= obstacle[4]) and \
                            (obstacle[2] <= z <= obstacle[5]):
                        return True

                    t = round(t + 0.01, 2)

        return False
