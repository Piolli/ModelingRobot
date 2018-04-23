import time
import xlsxwriter
# from xlsxwriter_base import *


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

        # For create n=0 row for table
        self.first_start_method = True

        # For create report of data
        self.report = open("/Users/alexandr/Desktop/Моделирование информационных процессов/MainProject/base/report.txt",
                           mode="w", encoding="UTF-8")

        # For draw start and end conf points
        self.q0 = conf_space.q0
        self.qT = conf_space.qT

        # Excel writer
        self.workbook = xlsxwriter.Workbook('arrays.xlsx')
        # self.workbook = Workbook('arrays1.xlsx')
        self.worksheet = self.workbook.add_worksheet()
        self.excel_row = 2
        self.excel_column = 1
        self.write_to_excel_titles()

        self.my_full_search(self.q0, self.qT)

    def write_to_excel_titles(self):
        self.worksheet.write_row(self.excel_row - 1, self.excel_column, ["n", "qn", "qT", "ZAPR", "L(qn, qT)"])

    def write_to_file_excel(self, qn, L, increment=True):
        n = self.excel_row - 2
        data = [n, qn, self.qT, self.forbidden_points, L]
        for column in range(self.excel_column, 6):
            self.worksheet.write_string(self.excel_row, column, str(data.pop(0)))
        if increment:
            self.excel_row += 1

    def my_full_search(self, q0, qT):
        if self.complete_path_is_finded or self.is_show_data_path:
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
                print("Список 'открыт' пуст")
                self.complete_path_is_finded = True
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

        if self.first_start_method:
            self.write_to_file_excel(str(self.q0), full_search_path, increment=True)
            self.first_start_method = False
        else:
            n = self.excel_row - 2
            self.worksheet.write_string(self.excel_row, 5, str(full_search_path))
            self.excel_row += 1


        good_path_is_finded = False

        if not self.complete_path_is_finded:
            for i in range(len(full_search_path)):
                point = full_search_path[i]

                if self.check_is_on_obstacle(point, 100, self.obstacles):
                    previous_point = full_search_path[i - 1]
                    self.forbidden_points.append(point)

                    point_neighbours = self.conf_space.neighbours(previous_point)
                    for neighbour in point_neighbours:
                        if self.check_is_on_obstacle(neighbour, 100, self.obstacles) and neighbour not in self.forbidden_points:
                            self.forbidden_points.append(neighbour)

                    self.report.write("n: %d\n" % (len(self.forbidden_points) - 1))
                    self.report.write("ZAPR: %s\n" % self.forbidden_points)
                    self.report.write("L(qn, qT): %s\n" % full_search_path)
                    self.change_path_points.append(previous_point)
                    self.report.write("qn: %s\n-----------------------------------\n" % previous_point)
                    # self.write_to_file_excel(previous_point, full_search_path)
                    n = self.excel_row - 2
                    data = [n, previous_point, self.qT, self.forbidden_points]
                    # print(data, "-----------------")
                    for column in range(self.excel_column, 5):
                        self.worksheet.write_string(self.excel_row, column, str(data.pop(0)))

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
                        good_path_is_finded = True
                        break

        self.clear_previous_path()

        # self.conf_space.draw_path(self.change_path_points, color="darkgreen")


        self.complete_path.append(qT)
        # self.conf_space.draw_path(self.complete_path)
        self.draw_start_end_points()

        if good_path_is_finded and not self.is_show_data_path:
            del self.complete_path[-1]
            del self.complete_path[0]

            self.conf_space.draw_path(self.complete_path)
            self.conf_space.draw_path(self.forbidden_points, color="red")
            self.draw_start_end_points()
            self.report.write("Путь найден: %s\n" % str(self.complete_path))
            self.report.write("Затраченное время: %d сек." % float(time.time() - self.start_time))
            self.worksheet.write_string(self.excel_row + 1, self.excel_column,
                                        "Пройденный путь: " + str(self.complete_path))
            self.worksheet.write_string(self.excel_row + 2, self.excel_column, "Затраченное время: " + str(
                round(float(time.time() - self.start_time), 3)) + " сек")
            self.is_show_data_path = True
        elif self.complete_path_is_finded and not self.is_show_data_path:
            for point in self.change_path_points:
                self.conf_space.canvas.delete(point)

            print("Путь не найден")
            self.draw_start_end_points()

            # For delete IV part of coordinate system points
            # custom_forbidden = []
            # for i in range(len(self.forbidden_points)):
            #     if not(self.forbidden_points[i][0] > 0 and self.forbidden_points[i][1] < 0):
            #         custom_forbidden.append(self.forbidden_points[i])
            # self.conf_space.draw_path(custom_forbidden, color="red")

            self.conf_space.draw_path(self.forbidden_points, color="red")

            self.is_show_data_path = True
            self.report.write("Путь не может быть найден!\n")
            self.report.write("Затраченное время: %d сек." % (time.time() - self.start_time))
            self.worksheet.write_string(self.excel_row + 1, self.excel_column, "Путь не может быть найден")
            self.worksheet.write_string(self.excel_row + 2, self.excel_column, "Затраченное время: " + str(
                round(float(time.time() - self.start_time), 3)) + " сек")

        self.report.close()
        self.workbook.close()

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
        for i in range(self.conf_space.n):
            if point[i] <= border[0] or point[i] >= border[1]:
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
