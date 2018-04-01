import base.matrixutils as utils
import math as m


class Vector3D:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    # def to_isometric(self):
    #     # Custom isometric
    #     a = m.radians(-45)
    #     b = m.radians(45)
    #
    #     matr1 = utils.to_matrix(3, [1, 0, 0,
    #                                 0, m.cos(a), m.sin(a),
    #                                 0, -m.sin(a), m.cos(a)])
    #
    #     matr2 = utils.to_matrix(3, [m.cos(b), 0, -m.sin(b),
    #                                 0, 1, 0,
    #                                 m.sin(b), 0, m.cos(b)])
    #
    #     matr_mult_12 = utils.matrixmult(matr1, matr2)
    #
    #     custom_isometric = matr_mult_12
    #     # ----------------
    #
    #     # values_matr_isometric = [m.sqrt(3), 0, -m.sqrt(3),
    #     #                          1, 2, 1,
    #     #                          m.sqrt(2), -m.sqrt(2), m.sqrt(2)]
    #     # # Multiply on coefficient
    #     # for i in range(len(values_matr_isometric)):
    #     #     values_matr_isometric[i] *= (1 / m.sqrt(6))
    #     #
    #     # isometric_translate_matrix = utils.to_matrix(3, values_matr_isometric)
    #
    #     vector3d = utils.to_matrix(1, [self.y, self.z, self.x])
    #
    #     orthogonal_translate_matrix = utils.to_matrix(3, [1, 0, 0,
    #                                                       0, 1, 0,
    #                                                       0, 0, 0])
    #
    #     # vector_c = (1 / m.sqrt(6)) * utils.matrixmult(isometric_translate_matrix, vector3d)
    #     # -----Custom
    #     isometric_translate_matrix = custom_isometric
    #     # -----------
    #     vector_c = utils.matrixmult(isometric_translate_matrix, vector3d)
    #     vector_b = utils.matrixmult(orthogonal_translate_matrix, vector_c)
    #
    #     return Vector3D(vector_b[0][0], vector_b[1][0], vector_b[2][0])

    def to_isometric(self):
        cavaluer_proj = utils.to_matrix(4, [1, 0, -0.65, 0,
                                            0, 1, -0.65, 0,
                                            0, 0, 0, 0,
                                            0, 0, 0, 1])

        world = utils.to_matrix(1, [self.x, self.y, self.z, 1])

        ortho_proj = utils.to_matrix(4, [1, 0, 0, 0,
                                         0, 1, 0, 0,
                                         0, 0, 0, 0,
                                         0, 0, 0, 1])

        world = utils.to_matrix(1, [world[1][0], world[2][0], world[0][0], 1])
        ortho = utils.matrixmult(ortho_proj, utils.matrixmult(cavaluer_proj, world))

        return Vector3D(ortho[0][0], ortho[1][0], ortho[2][0])

    def __str__(self) -> str:
        return "x: {0} y: {1} z: {2}".format(self.x, self.y, self.z)

    def rotate_around_point(self, a, v0):
        a = a * m.pi / 180
        self.x = v0.x + (self.x - v0.x) * m.cos(a) - (self.y - v0.y) * m.sin(a)
        self.y = v0.y + (self.y - v0.y) * m.cos(a) + (self.x - v0.x) * m.sin(a)

        return Vector3D(self.x, self.y, self.z)

    def rotate_around(self, angle, p):
        rad = angle * m.pi / 180
        s = m.sin(rad)
        c = m.cos(rad)

        self.x -= p.x
        self.y -= p.y

        x_new = self.x * c - self.y * s
        y_new = self.x * s + self.y * c

        self.x = x_new + p.x
        self.y = y_new + p.y

        return Vector3D(self.x, self.y, self.z)

    def simple_rotate(self, angle, v):
        self.x -= v.x
        self.y -= v.y
        self.z -= v.z

        rad = angle * m.pi / 180
        cosa = m.cos(rad)
        sina = m.sin(rad)
        z = self.z * cosa - self.x * sina
        x = self.z * sina + self.x * cosa

        self.x = v.x + x
        self.z = v.z + z
        self.y += v.y

        return Vector3D(x, self.y, z)

    def rotateY(self, angle):
        """ Rotates the point around the Y axis by the given angle in degrees. """
        rad = angle * m.pi / 180
        cosa = m.cos(rad)
        sina = m.sin(rad)
        z = self.z * cosa - self.x * sina
        x = self.z * sina + self.x * cosa
        return Vector3D(x, self.y, z)

    def translate(self, x=0, y=0, z=0):
        return Vector3D(self.x + x, self.y + y, self.z + z)

    def rotate(origin, point, angle):
        """
        Rotate a point counterclockwise by a given angle around a given origin.

        The angle should be given in radians.
        """
        ox, oy = origin
        px, py = point

        qx = ox + m.cos(angle) * (px - ox) - m.sin(angle) * (py - oy)
        qy = oy + m.sin(angle) * (px - ox) + m.cos(angle) * (py - oy)
        return qx, qy

    def rotateX(self, angle):
        rad = angle * m.pi / 180
        c = m.cos(rad)
        s = m.sin(rad)
        oldY = self.y
        self.y = 0
        matrix = utils.to_matrix(3, [1, 0, 0,
                                     0, c, -s,
                                     0, s, c])
        v = utils.to_matrix(1, [self.x, self.y, self.z])

        # print("matrix:", matrix, " vector:", v)

        result = utils.matrixmult(matrix, v)
        result[1][0] += oldY

        return Vector3D(result[0][0], result[1][0], result[2][0])

    def rotate_y(self, angle):
        angle = angle * m.pi / 180
        # """Rotate by y"""
        rotate_matrix = utils.to_matrix(3, [
            m.cos(angle), 0, m.sin(angle),
            0, 1, 0,
            -m.sin(angle), 0, m.cos(angle)])

        # """Rotate by z"""
        # rotate_matrix = utils.to_matrix(3, [
        #                                 m.cos(angle), m.sin(angle), 0,
        #                                 -m.sin(angle), m.cos(angle), 0,
        #                                 0, 0, 1
        #                             ])

        # """Rotate by x"""
        # rotate_matrix = utils.to_matrix(3, [
        #                                1, 0, 0,
        #                                 0, m.cos(angle), -m.sin(angle),
        #                                 0, m.sin(angle), m.cos(angle)
        #                             ])

        vector3d = utils.to_matrix(1, [self.x, self.y, self.z])
        vector_matrix = utils.matrixmult(rotate_matrix, vector3d)

        self.x = vector_matrix[0][0]
        self.y = vector_matrix[1][0]
        self.z = vector_matrix[2][0]

        return Vector3D(vector_matrix[0][0], vector_matrix[1][0], vector_matrix[2][0])
