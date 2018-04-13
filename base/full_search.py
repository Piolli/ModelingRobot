import time


class FullSearch:
    def __init__(self, obstacles, conf_space, step_by_step):
        self.conf_space = conf_space
        self.obstacles = obstacles
        self.forbidden_points = []
        self.change_path_points = []
        self.complete_path = [conf_space.q0]
        self.count_change_path = 0
        self.complete_path_is_finded = False
        self.is_show_data_path = False
        self.previous_draw_points = []

        self.start_time = time.time()

        # For step by step finding path (bool)
        self.step_by_step = step_by_step

        # For create report of data
        self.report = open("/Users/alexandr/Desktop/Моделирование информационных процессов/MainProject/base/report.txt", mode="w", encoding="UTF-8")

        # For draw start and end conf points
        self.q0 = conf_space.q0
        self.qT = conf_space.qT

        self.my_full_search(self.q0, self.qT)

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

        if not self.complete_path_is_finded:
            for i in range(len(full_search_path)):
                point = full_search_path[i]
                if self.check_is_on_obstacle(point, 100, self.obstacles) and not self.is_show_data_path:
                    previous_point = full_search_path[i - 1]
                    self.forbidden_points.append(point)
                    self.report.write("Смена пути №%d\n-------------\n" % (len(self.forbidden_points)-1))
                    self.report.write("Ранее неизвестная запрещенная точка: %s\n" % point)
                    self.report.write("Путь: %s\n" % full_search_path)
                    self.change_path_points.append(previous_point)
                    self.report.write("Возвращаемся в предыдущую точку (точка смены пути) и начинаем сначала: %s\n-------------\n" % previous_point)

                    if self.step_by_step:
                        self.clear_previous_path()
                        self.conf_space.draw_path(self.complete_path)
                        self.previous_draw_points = self.conf_space.draw_path(full_search_path)
                        self.draw_start_end_points()
                        self.conf_space.draw_path(self.forbidden_points, color="red")
                        self.conf_space.draw_point(previous_point[0], previous_point[1], color="darkgreen")
                        self.conf_space.top.update()
                        time.sleep(0.5)

                    self.my_full_search(previous_point, qT)
                    return 0
                else:
                    # Adding previous point to complete_path
                    self.complete_path.append(point)
                    if point == self.qT:
                        self.complete_path_is_finded = True

        self.clear_previous_path()

        self.conf_space.draw_path(self.change_path_points, color="darkgreen")
        self.conf_space.draw_path(self.forbidden_points, color="red")

        self.complete_path.append(qT)
        self.conf_space.draw_path(self.complete_path)
        self.draw_start_end_points()

        if self.complete_path_is_finded and not self.is_show_data_path:
            self.report.write("Путь найден: %s\n" % full_search_path)
            self.report.write("Затраченное время: %d сек." % (time.time() - self.start_time))
            self.is_show_data_path = True
        elif not self.complete_path_is_finded and not self.is_show_data_path:
            print("Путь не найден")
            self.is_show_data_path = True
            self.report.write("Путь не может быть найден!\n")
            self.report.write("Затраченное время: %d сек." % (time.time() - self.start_time))

        self.report.close()

        return 0

    def draw_start_end_points(self):
        self.conf_space.draw_point(self.q0[0], self.q0[1], color="green")
        self.conf_space.draw_point(self.qT[0], self.qT[1], color="yellow")

    def clear_previous_path(self):
        for point in self.previous_draw_points:
            self.conf_space.canvas.delete(point)
        self.conf_space.top.update()

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

    def check_is_on_obstacle(self, q, lenght, obstacles) -> bool:
        if len(obstacles) == 0:
            return False

        lenght = 100

        for obstacle in obstacles:
            for i in range(self.conf_space.n):
                t = 0
                point_i = self.conf_space.get_manipulator_position(i, q, lenght)
                point_i1 = self.conf_space.get_manipulator_position(i + 1, q, lenght)
                while t <= 1:

                    x = point_i1[0][0] + (point_i[0][0] - point_i1[0][0]) * t
                    y = point_i1[1][0] + (point_i[1][0] - point_i1[1][0]) * t
                    z = point_i1[2][0] + (point_i[2][0] - point_i1[2][0]) * t

                    if (obstacle[0] <= x <= obstacle[3]) and \
                            (obstacle[1] <= y <= obstacle[4]) and \
                            (obstacle[2] <= z <= obstacle[5]):
                        return True

                    t = round(t + 0.01, 2)

        return False
