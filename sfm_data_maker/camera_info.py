# -*- coding:utf-8 -*-
# 添加相机信息

from enum import Enum


class ImageOrientation(Enum):
    # 0th-Row_0th-Column
    Top_Left = 1,
    Top_Right = 2,
    Bottom_Right = 3,
    Bottom_Left = 4,
    Left_Top = 5,
    Right_Top = 6,
    Right_Bottom = 7,
    Left_Bottom = 8


class SfMCamera(object):
    def __init__(self, camera_id, maker, model, projection_type="brown"):
        self._camera_id = camera_id
        self._maker = maker
        self._model = model
        # perspective/brown/fisheye/equirectangular/spherical
        self._projection_type = projection_type

        self._k1 = 0
        self._k2 = 0
        self._k3 = 0
        self._p1 = 0
        self._p2 = 0
        self._k1_prior = 0
        self._k2_prior = 0
        self._k3_prior = 0
        self._p1_prior = 0
        self._p2_prior = 0

        self._focal_x = 0
        self._focal_y = 0

        self._focal_x_prior = 0
        self._focal_y_prior = 0

        self._cx = 0
        self._cy = 0
        self._cx_prior = 0
        self._cy_prior = 0

        self._width = 2448
        self._height = 2048

        self._focal_prior = 0
        self._focal = 0

        # flag: origin position(0,0) of image
        self._orientation = 1

    @property
    def camera_id(self):
        return self._camera_id

    @camera_id.setter
    def camera_id(self, value):
        self._camera_id = value

    @property
    def maker(self):
        return self._maker

    @maker.setter
    def maker(self, value):
        self._maker = value

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, value):
        self._model = value

    @property
    def projection_type(self):
        return self._projection_type

    @projection_type.setter
    def projection_type(self, value):
        self._projection_type = value

    @property
    def k1(self):
        return self._k1

    @k1.setter
    def k1(self, value):
        self._k1 = value

    @property
    def k2(self):
        return self._k2

    @k2.setter
    def k2(self, value):
        self._k2 = value

    @property
    def k3(self):
        return self._k3

    @k3.setter
    def k3(self, value):
        self._k3 = value

    @property
    def p1(self):
        return self._p1

    @p1.setter
    def p1(self, value):
        self._p1 = value

    @property
    def p2(self):
        return self._p2

    @p2.setter
    def p2(self, value):
        self._p2 = value

    @property
    def k1_prior(self):
        return self._k1_prior

    @k1_prior.setter
    def k1_prior(self, value):
        self._k1_prior = value

    @property
    def k2_prior(self):
        return self._k2_prior

    @k2_prior.setter
    def k2_prior(self, value):
        self._k2_prior = value

    @property
    def k3_prior(self):
        return self._k3_prior

    @k3_prior.setter
    def k3_prior(self, value):
        self._k3_prior = value

    @property
    def p1_prior(self):
        return self._p1_prior

    @p1_prior.setter
    def p1_prior(self, value):
        self._p1_prior = value

    @property
    def p2_prior(self):
        return self._p2_prior

    @p2_prior.setter
    def p2_prior(self, value):
        self._p2_prior = value

    @property
    def focal_x(self):
        return self._focal_x

    @focal_x.setter
    def focal_x(self, value):
        self._focal_x = value

    @property
    def focal_y(self):
        return self._focal_y

    @focal_y.setter
    def focal_y(self, value):
        self._focal_y = value

    @property
    def focal_x_prior(self):
        return self._focal_x_prior

    @focal_x_prior.setter
    def focal_x_prior(self, value):
        self._focal_x_prior = value

    @property
    def focal_y_prior(self):
        return self._focal_y_prior

    @focal_y_prior.setter
    def focal_y_prior(self, value):
        self._focal_y_prior = value

    @property
    def cx(self):
        return self._cx

    @cx.setter
    def cx(self, value):
        self._cx = value

    @property
    def cy(self):
        return self._cy

    @cy.setter
    def cy(self, value):
        self._cy = value

    @property
    def cx_prior(self):
        return self._cx_prior

    @cx_prior.setter
    def cx_prior(self, value):
        self._cx_prior = value

    @property
    def cy_prior(self):
        return self._cy_prior

    @cy_prior.setter
    def cy_prior(self, value):
        self._cy_prior = value

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        self._width = value

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = value

    @property
    def orientation(self):
        return self._orientation

    @orientation.setter
    def orientation(self, value):
        self._orientation = value

    @property
    def focal(self):
        return self._focal

    @focal.setter
    def focal(self, value):
        self._focal = value

    @property
    def focal_prior(self):
        return self._focal_prior

    @focal_prior.setter
    def focal_prior(self, value):
        self._focal_prior = value

    def make_camera_model(self):
        camera_model = {
            str(self._camera_id): {
                "projection_type": self._projection_type,
                "width": self._width,
                "height": self._height,
                "k1": self._k1_prior,
                "k2": self._k2_prior,
                "k3": self._k3_prior,
                "p1": self._p1_prior,
                "p2": self._p2_prior,
                "k1_prior": self._k1_prior,
                "k2_prior": self._k2_prior,
                "k3_prior": self._k3_prior,
                "p1_prior": self._p1_prior,
                "p2_prior": self._p2_prior,
                "focal": self._focal_prior,
                "focal_prior": self._focal_prior,
                "focal_x": self._focal_x_prior,
                "focal_y": self._focal_y_prior,
                "c_x": self._cx_prior,
                "c_y": self._cy_prior,
                "focal_x_prior": self._focal_x_prior,
                "focal_y_prior": self._focal_y_prior,
                "c_x_prior": self._cx_prior,
                "c_y_prior": self._cy_prior,
            }
        }
        return camera_model
