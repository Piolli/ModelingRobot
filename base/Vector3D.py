import base.matrixutils as utils
import math as m


class Vector3D:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def to_isometric(self):
        values_matr_isometric = [m.sqrt(3), 0, -m.sqrt(3),
                                1, 2, 1,
                                m.sqrt(2), -m.sqrt(2), m.sqrt(2)]
        #Multiply on coefficient
        for i in range(len(values_matr_isometric)):
            values_matr_isometric[i] *= (1 / m.sqrt(6))

        isometric_translate_matrix = utils.to_matrix(3, values_matr_isometric)

        vector3d = utils.to_matrix(1, [self.x, self.y, self.z])

        orthogonal_translate_matrix = utils.to_matrix(3, [1, 0, 0,
                                                          0, 1, 0,
                                                          0, 0, 0])

        # vector_c = (1 / m.sqrt(6)) * utils.matrixmult(isometric_translate_matrix, vector3d)
        vector_c = utils.matrixmult(isometric_translate_matrix, vector3d)
        vector_b = utils.matrixmult(orthogonal_translate_matrix, vector_c)

        return Vector3D(vector_b[0][0], vector_b[1][0], vector_b[2][0])

    def __str__(self) -> str:
        return "x: {0} y: {1} z: {2}".format(self.x, self.y, self.z)

    def rotate_y(self, angle):
        angle = m.radians(angle)
        """Rotate by y"""
        rotate_matrix = utils.to_matrix(3, [
                                        m.cos(angle), 0, m.sin(angle),
                                        0, 1, 0,
                                        -m.sin(angle), 0, m.cos(angle)])

        """Rotate by z"""
        # rotate_matrix = utils.to_matrix(3, [
        #                                 m.cos(angle), m.sin(angle), 0,
        #                                 -m.sin(angle), m.cos(angle), 0,
        #                                 0, 0, 1
        #                             ])

        """Rotate by x"""
        # rotate_matrix = utils.to_matrix(3, [
        #                                1, 0, 0,
        #                                 0, m.cos(angle), -m.sin(angle),
        #                                 0, m.sin(angle), m.cos(angle)
        #                             ])

        vector3d = utils.to_matrix(1, [self.x, self.y, self.z])
        vector_matrix = utils.matrixmult(rotate_matrix, vector3d)

        return Vector3D(vector_matrix[0][0], vector_matrix[1][0], vector_matrix[2][0])

