import base.Vector3D as v
import base.logix as d


class Rectangle:
    """s - start vector, e - end vector"""

    def __init__(self, s: v.Vector3D, e: v.Vector3D) -> None:
        self.__start = s
        self.__end = e
        height = e.y - s.y
        width_x = e.x - s.x
        width_z = e.z - s.z

        self.vc1 = s
        self.vc2 = s.translate(y=height)
        self.vc3 = s.translate(y=height, z=width_z)
        self.vc4 = s.translate(z=width_z)
        self.vc5 = s.translate(x=width_x, z=width_z)
        self.vc6 = s.translate(x=width_x)
        self.vc7 = s.translate(x=width_x, y=height)
        self.vc8 = e

        self.points = [self.vc1, self.vc2, self.vc3, self.vc4,
                       self.vc5, self.vc6, self.vc7, self.vc8]

        # for i in range(0, 8):
        #     print("vc" + str(i+1), self.points[i])

    def draw(self, divjok: d.Divjok):
        # DRAW NUMBER ABOUT OF EACH TOP OF CUBE
        # divjok.create_text_v( self.points[0].to_isometric(), "1", -10, 5)
        # divjok.create_text_v( self.points[1].to_isometric(), "2", -10, 5)
        # divjok.create_text_v( self.points[2].to_isometric(), "3", 5, 5)
        # divjok.create_text_v( self.points[3].to_isometric(), "4", 5, 5)
        # divjok.create_text_v( self.points[4].to_isometric(), "5", 5, 5)
        # divjok.create_text_v( self.points[5].to_isometric(), "6", 5, -10)
        # divjok.create_text_v( self.points[6].to_isometric(), "7", 10, -10)
        # divjok.create_text_v( self.points[7].to_isometric(), "8", 10, 5)


        divjok.create_line_v(self.points[0].to_isometric(),  self.points[1].to_isometric())
        divjok.create_line_v(self.points[2].to_isometric(),  self.points[3].to_isometric())
        divjok.create_line_v(self.points[0].to_isometric(),  self.points[3].to_isometric())
        divjok.create_line_v(self.points[1].to_isometric(),  self.points[2].to_isometric())
        divjok.create_line_v(self.points[1].to_isometric(),  self.points[6].to_isometric())
        divjok.create_line_v(self.points[0].to_isometric(),  self.points[5].to_isometric())
        divjok.create_line_v(self.points[6].to_isometric(),  self.points[5].to_isometric())
        divjok.create_line_v(self.points[6].to_isometric(),  self.points[7].to_isometric())
        divjok.create_line_v(self.points[7].to_isometric(),  self.points[4].to_isometric())
        divjok.create_line_v(self.points[3].to_isometric(),  self.points[4].to_isometric())
        divjok.create_line_v(self.points[5].to_isometric(),  self.points[4].to_isometric())
        divjok.create_line_v(self.points[2].to_isometric(),  self.points[7].to_isometric())

        # Fill start point and end point
        divjok.create_point_v(self.__start.to_isometric())
        divjok.create_point_v(self.__end.to_isometric())

    def rotate_y(self, angle):
        for i in range(0, 8):
            self.points[i] = self.points[i].rotateY(angle)
