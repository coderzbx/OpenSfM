# -*- coding:utf-8 -*-


class Point(object):
    def __init__(self, x, y, z):
        self._x = x
        self._y = y
        self._z = z

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, x):
        self._x = x

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, y):
        self._y = y

    @property
    def z(self):
        return self._z

    @z.setter
    def z(self, z):
        self._z = z


class TrackPoint(object):
    def __init__(self):
        self._track_point_id = ""
        self._track_id = ""
        self._task_id = ""
        self._seq = ""

        self._coord = Point(0, 0, 0)
        self._utm_zone = ""
        self._utm_coord = Point(0, 0, 0)
        self._device_type = ""

        self._status = 0
        self._image_width = 2448
        self._image_height = 2048
        self._del_flag = 0
        self._loc_time = 0
        self._north_velocity = 0
        self._east_velocity = 0
        self._up_velocity = 0
        self._roll = 0
        self._pitch = 0
        self._azimuth = 0
        self._longitude_sigma = 0
        self._latitude_sigma = 0
        self._height_sigma = 0
        self._roll_sigma = 0
        self._pitch_sigma = 0
        self._azimuth_sigma = 0
        self._position_type = 0

        self._R = []
        self._T = []
        self._C = []

        self._post_difference = False
        self._amb_status = 1
        self._quality_num = 1
        self._gps_status = 1
        self._imu_status = 1

    @property
    def track_point_id(self):
        return self._track_point_id

    @track_point_id.setter
    def track_point_id(self, value):
        self._track_point_id = value

    @property
    def track_id(self):
        return self._track_id

    @track_id.setter
    def track_id(self, value):
        self._track_id = value

    @property
    def task_id(self):
        return self._task_id

    @task_id.setter
    def task_id(self, value):
        self._task_id = value

    @property
    def seq(self):
        return self._seq

    @seq.setter
    def seq(self, value):
        self._seq = value

    @property
    def device_type(self):
        return self._device_type

    @device_type.setter
    def device_type(self, value):
        self._device_type = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value

    @property
    def position_type(self):
        return self._position_type

    @position_type.setter
    def position_type(self, value):
        self._position_type = value

    @property
    def image_width(self):
        return self._image_width

    @image_width.setter
    def image_width(self, value):
        self._image_width = value

    @property
    def image_height(self):
        return self._image_height

    @image_height.setter
    def image_height(self, value):
        self._image_height = value

    @property
    def del_flag(self):
        return self._del_flag

    @del_flag.setter
    def del_flag(self, value):
        self._del_flag = value

    @property
    def coord(self):
        return self._coord

    @coord.setter
    def coord(self, value):
        self._coord = value

    @property
    def utm_coord(self):
        return self._utm_coord

    @utm_coord.setter
    def utm_coord(self, value):
        self._utm_coord = value

    @property
    def utm_zone(self):
        return self._utm_zone

    @utm_zone.setter
    def utm_zone(self, value):
        self._utm_zone = value

    @property
    def loc_time(self):
        return self._loc_time

    @loc_time.setter
    def loc_time(self, value):
        self._loc_time = value

    @property
    def north_velocity(self):
        return self._north_velocity

    @north_velocity.setter
    def north_velocity(self, value):
        self._north_velocity = value

    @property
    def east_velocity(self):
        return self._east_velocity

    @east_velocity.setter
    def east_velocity(self, value):
        self._east_velocity = value

    @property
    def up_velocity(self):
        return self._up_velocity

    @up_velocity.setter
    def up_velocity(self, value):
        self._up_velocity = value

    @property
    def roll(self):
        return self._roll

    @roll.setter
    def roll(self, value):
        self._roll = value

    @property
    def pitch(self):
        return self._pitch

    @pitch.setter
    def pitch(self, value):
        self._pitch = value

    @property
    def azimuth(self):
        return self._azimuth

    @azimuth.setter
    def azimuth(self, value):
        self._azimuth = value

    @property
    def longitude_sigma(self):
        return self._longitude_sigma

    @longitude_sigma.setter
    def longitude_sigma(self, value):
        self._longitude_sigma = value

    @property
    def latitude_sigma(self):
        return self._latitude_sigma

    @latitude_sigma.setter
    def latitude_sigma(self, value):
        self._latitude_sigma = value

    @property
    def height_sigma(self):
        return self._height_sigma

    @height_sigma.setter
    def height_sigma(self, value):
        self._height_sigma = value

    @property
    def roll_sigma(self):
        return self._roll_sigma

    @roll_sigma.setter
    def roll_sigma(self, value):
        self._roll_sigma = value

    @property
    def pitch_sigma(self):
        return self._pitch_sigma

    @pitch_sigma.setter
    def pitch_sigma(self, value):
        self._pitch_sigma = value

    @property
    def azimuth_sigma(self):
        return self._azimuth_sigma

    @azimuth_sigma.setter
    def azimuth_sigma(self, value):
        self._azimuth_sigma = value

    @property
    def R(self):
        return self._R

    @R.setter
    def R(self, value):
        self._R = value

    @property
    def T(self):
        return self._T

    @T.setter
    def T(self, value):
        self._T = value

    @property
    def C(self):
        return self._C

    @C.setter
    def C(self, value):
        self._C = value

    @property
    def post_difference(self):
        return self._post_difference

    @post_difference.setter
    def post_difference(self, value):
        self._post_difference = value

    @property
    def amb_status(self):
        return self._amb_status

    @amb_status.setter
    def amb_status(self, value):
        self._amb_status = value

    @property
    def quality_num(self):
        return self._quality_num

    @quality_num.setter
    def quality_num(self, value):
        self._quality_num = value

    @property
    def gps_status(self):
        return self._gps_status

    @gps_status.setter
    def gps_status(self, value):
        self._gps_status = value

    @property
    def imu_status(self):
        return self._imu_status

    @imu_status.setter
    def imu_status(self, value):
        self._imu_status = value


class TrackPointExtendInfo(object):
    def __init__(self, track_point_id, track_id, ground_height, delta_x=0, delta_y=0, delta_z=0,
                 delta_roll=0, delta_pitch=0, delta_azimuth=0, project_id=""):
        self._track_point_id = track_point_id
        self._track_id = track_id
        self._ground_height = ground_height
        self._delta_x = delta_x
        self._delta_y = delta_y
        self._delta_z = delta_z
        self._delta_roll = delta_roll
        self._delta_pitch = delta_pitch
        self._delta_azimuth = delta_azimuth
        self._project_id = project_id

    @property
    def track_point_id(self):
        return self._track_point_id

    @property
    def track_id(self):
        return self._track_id

    @property
    def ground_height(self):
        return self._ground_height

    @property
    def delta_x(self):
        return self._delta_x

    @property
    def delta_y(self):
        return self._delta_y

    @property
    def delta_z(self):
        return self._delta_z

    @property
    def delta_roll(self):
        return self._delta_roll

    @property
    def delta_pitch(self):
        return self._delta_pitch

    @property
    def delta_azimuth(self):
        return self._delta_azimuth

    @property
    def project_id(self):
        return self._project_id


class Track(object):
    def __init__(self):
        self._track_point_list = []
        self._task_id = ""
        self._track_shape = []
        self._device_id = ""
        self._track_id = ""
        self._seq = ""
        self._total_mileage = 0

    @property
    def track_point_list(self):
        return self._track_point_list

    @property
    def task_id(self):
        return self._task_id

    @task_id.setter
    def task_id(self, task_id):
        self._task_id = task_id

    @property
    def seq(self):
        return self._seq

    @seq.setter
    def seq(self, value):
        self._seq = value

    @property
    def track_id(self):
        return self._track_id

    @track_id.setter
    def track_id(self, value):
        self._track_id = value

    @property
    def total_mileage(self):
        return self._total_mileage

    @total_mileage.setter
    def total_mileage(self, value):
        self._total_mileage = value

    @property
    def track_shape(self):
        return self._track_shape

    @track_shape.setter
    def track_shape(self, track_shape):
        self._track_shape = track_shape

    @property
    def device_id(self):
        return self._device_id

    @device_id.setter
    def device_id(self, device_id):
        self._device_id = device_id

    def add_track_point(self, track_point):
        self._track_point_list.append(track_point)


class CameraDistortion(object):
    def __init__(self):
        self._k1 = 0
        self._k2 = 0
        self._k3 = 0
        self._p1 = 0
        self._p2 = 0

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


class CameraParams(object):
    def __init__(self):
        self._focus_x = 0
        self._focus_y = 0
        self._principle_point_x = 0
        self._principle_point_y = 0
        self._camera_distortion = CameraDistortion()
        self._image_dimensions = []

    @property
    def focus_x(self):
        return self._focus_x

    @focus_x.setter
    def focus_x(self, value):
        self._focus_x = value

    @property
    def focus_y(self):
        return self._focus_y

    @focus_y.setter
    def focus_y(self, value):
        self._focus_y = value

    @property
    def principle_point_x(self):
        return self._principle_point_x

    @principle_point_x.setter
    def principle_point_x(self, value):
        self._principle_point_x = value

    @property
    def principle_point_y(self):
        return self._principle_point_y

    @principle_point_y.setter
    def principle_point_y(self, value):
        self._principle_point_y = value

    @property
    def camera_distortion(self):
        return self._camera_distortion

    @camera_distortion.setter
    def camera_distortion(self, value):
        self._camera_distortion = value

    @property
    def image_dimensions(self):
        return self._image_dimensions

    @image_dimensions.setter
    def image_dimensions(self, value):
        self._image_dimensions = value


class CameraAdjustParams(object):
    def __init__(self):
        self._focus = 0
        self._base_line = 0
        self._principle_point_x = 0
        self._principle_point_y = 0
        self._image_dimensions = []

    @property
    def focus(self):
        return self._focus

    @focus.setter
    def focus(self, value):
        self._focus = value

    @property
    def base_line(self):
        return self._base_line

    @base_line.setter
    def base_line(self, value):
        self._base_line = value

    @property
    def principle_point_x(self):
        return self._principle_point_x

    @principle_point_x.setter
    def principle_point_x(self, value):
        self._principle_point_x = value

    @property
    def principle_point_y(self):
        return self._principle_point_y

    @principle_point_y.setter
    def principle_point_y(self, value):
        self._principle_point_y = value

    @property
    def image_dimensions(self):
        return self._image_dimensions

    @image_dimensions.setter
    def image_dimensions(self, value):
        self._image_dimensions = value


class Camera(object):
    def __init__(self):
        self._device_id = ""
        self._camera_type = ""
        self._version = ""
        self._upload_time = 0
        self._camera_params = {}
        self._adjust_params = CameraAdjustParams()

    @property
    def device_id(self):
        return self._device_id

    @device_id.setter
    def device_id(self, value):
        self._device_id = value

    @property
    def camera_type(self):
        return self._camera_type

    @camera_type.setter
    def camera_type(self, value):
        self._camera_type = value

    @property
    def version(self):
        return self._version

    @version.setter
    def version(self, value):
        self._version = value

    @property
    def upload_time(self):
        return self._upload_time

    @upload_time.setter
    def upload_time(self, value):
        self._upload_time = value

    @property
    def camera_params(self):
        return self._camera_params

    @camera_params.setter
    def camera_params(self, value):
        self._camera_params = value

    @property
    def adjust_params(self):
        return self._adjust_params

    @adjust_params.setter
    def adjust_params(self, value):
        self._adjust_params = value


class CameraExtendInfo(object):
    def __init__(self):
        self._camera_height = 0
        self._roll_delta = 0
        self._pitch_delta = 0
        self._azimuth_delta = 0

    @property
    def camera_height(self):
        return self._camera_height

    @camera_height.setter
    def camera_height(self, value):
        self._camera_height = value

    @property
    def roll_delta(self):
        return self._roll_delta

    @roll_delta.setter
    def roll_delta(self, value):
        self._roll_delta = value

    @property
    def pitch_delta(self):
        return self._pitch_delta

    @pitch_delta.setter
    def pitch_delta(self, value):
        self._pitch_delta = value

    @property
    def azimuth_delta(self):
        return self._azimuth_delta

    @azimuth_delta.setter
    def azimuth_delta(self, value):
        self._azimuth_delta = value


class LocDevice(object):
    def __init__(self):
        self._device_id = ""
        self._device_type = ""

    @property
    def device_id(self):
        return self._device_id

    @device_id.setter
    def device_id(self, value):
        self._device_id = value

    @property
    def device_type(self):
        return self._device_type

    @device_type.setter
    def device_type(self, value):
        self._device_type = value


class Device(object):
    def __init__(self):
        self._device_id = 0
        self._camera_map = {}
        self._loc_device_map = {}

    @property
    def device_id(self):
        return self._device_id

    @device_id.setter
    def device_id(self, value):
        self._device_id = value

    @property
    def camera_map(self):
        return self._camera_map

    @camera_map.setter
    def camera_map(self, value):
        self._camera_map = value

    @property
    def loc_device_map(self):
        return self._loc_device_map

    @loc_device_map.setter
    def loc_device_map(self, value):
        self._loc_device_map = value
