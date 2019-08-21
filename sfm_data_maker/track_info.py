# -*- coding:utf-8 -*-
import os
import json

import numpy as np

from defines import Point, TrackPoint, Track, Camera, CameraParams
from device_info import DeviceInfo
from camera_info import SfMCamera


class TrackInfo(object):
    def __init__(self, track_dir, track_id, reverse=False):
        self._track_dir = track_dir
        self._track_id = track_id
        self._reverse = reverse
        self._device = None
        self._camera = None
        self._track = None
        self._sfm_camera = None

    @property
    def device(self):
        return self._device

    @property
    def camera(self):
        return self._camera

    @property
    def track(self):
        return self._track

    @property
    def sfm_camera(self):
        return self._sfm_camera

    @property
    def reverse(self):
        return self._reverse

    @reverse.setter
    def reverse(self, value):
        self._reverse = value

    def parse_track(self):
        track_dir_name = "test_{}".format(self._track_id)
        track_json_path = os.path.join(self._track_dir, track_dir_name, "track.json")
        if not os.path.exists(track_json_path):
            return

        with open(track_json_path, "r") as f:
            json_data = json.load(f)

        track = Track()
        if "taskId" in json_data:
            track.task_id = json_data["taskId"]
        if "trackShape" in json_data:
            track_shape = []
            for point_info in json_data["trackShape"]:
                pt = Point(float(point_info["x"]), float(point_info["y"]), float(point_info["z"]))
                track_shape.append(pt)
            track.track_shape = track_shape
        if "deviceId" in json_data:
            track.device_id = json_data["deviceId"]
        if "trackId" in json_data:
            track.track_id = json_data["trackId"]
        if "totalMileage" in json_data:
            track.total_mileage = float(json_data["totalMileage"])
        if "seq" in json_data:
            track.seq = json_data["seq"]

        point_list = []
        if "pointList" in json_data:
            point_list = json_data["pointList"]

        for point_info in point_list:
            track_point = TrackPoint()
            track_point.track_id = track.track_id
            track_point.task_id = track.task_id
            track_point.seq = track.seq

            if "trackPointId" in point_info:
                track_point.track_point_id = point_info["trackPointId"]
            if "coordinate" in point_info:
                coordinate = point_info["coordinate"]
                track_point.coord = Point(float(coordinate["x"]), float(coordinate["y"]), float(coordinate["z"]))
            if "deviceType" in point_info:
                track_point.device_type = point_info["deviceType"]
            if "status" in point_info:
                track_point.status = int(point_info["status"])
            if "positionType" in point_info:
                track_point.position_type = int(point_info["positionType"])
            if "picW" in point_info:
                track_point.image_width = int(point_info["picW"])
            if "picH" in point_info:
                track_point.image_height = int(point_info["picH"])
            if "delFlag" in point_info:
                track_point.del_flag = int(point_info["delFlag"])
            if "C" in point_info:
                coord_value = point_info["C"]
                track_point.C = [float(coord_value[0][0]), float(coord_value[1][0]), float(coord_value[2][0])]
                track_point.utm_coord = Point(track_point.C[0], track_point.C[1], track_point.C[2])
            if "T" in point_info:
                coord_value = point_info["T"]
                track_point.T = [float(coord_value[0][0]), float(coord_value[1][0]), float(coord_value[2][0])]
            if "R" in point_info:
                coord_value = point_info["R"]
                track_point.R = [[float(coord_value[0][0]), float(coord_value[0][1]), float(coord_value[0][2])],
                                 [float(coord_value[1][0]), float(coord_value[1][1]), float(coord_value[1][2])],
                                 [float(coord_value[2][0]), float(coord_value[2][1]), float(coord_value[2][2])]]
                # np_r = np.array(coord_value, np.double)
                # track_point.R = np.array(coord_value, np.double)
            if "utm" in point_info:
                track_point.utm_zone = point_info["utm"]
            if "locTime" in point_info:
                track_point.loc_time = int(point_info["locTime"])
            if "northVelocity" in point_info:
                track_point.north_velocity = float(point_info["northVelocity"])
            if "eastVelocity" in point_info:
                track_point.east_velocity = float(point_info["eastVelocity"])
            if "upVelocity" in point_info:
                track_point.up_velocity = float(point_info["upVelocity"])
            if "roll" in point_info:
                track_point.roll = float(point_info["roll"])
            if "pitch" in point_info:
                track_point.pitch = float(point_info["pitch"])
            if "azimuth" in point_info:
                track_point.azimuth = float(point_info["azimuth"])
            if "longitudeSigma" in point_info:
                track_point.longitude_sigma = float(point_info["longitudeSigma"])
            if "latitudeSigma" in point_info:
                track_point.latitude_sigma = float(point_info["latitudeSigma"])
            if "heightSigma" in point_info:
                track_point.height_sigma = float(point_info["heightSigma"])
            if "rollSigma" in point_info:
                track_point.roll_sigma = float(point_info["rollSigma"])
            if "pitchSigma" in point_info:
                track_point.pitch_sigma = float(point_info["pitchSigma"])
            if "azimuthSigma" in point_info:
                track_point.azimuth_sigma = float(point_info["azimuthSigma"])
            if "postDifference" in point_info:
                track_point.post_difference = int(point_info["postDifference"])
            if "ambStatus" in point_info:
                track_point.amb_status = int(point_info["ambStatus"])
            if "qualityNum" in point_info:
                track_point.quality_num = int(point_info["qualityNum"])
            track.add_track_point(track_point)

        self._track = track
        return track

    def parse_device(self):
        device_info = DeviceInfo(track_dir=self._track_dir, track_id=self._track_id)
        device = device_info.parse_device()
        self._device = device
        for k, v in device.camera_map.items():
            if not isinstance(v, Camera):
                return
            self._camera = v
        camera_params = self._camera.camera_params[self._camera.device_id]
        if not isinstance(camera_params, CameraParams):
            return
        #
        camera_id = device.device_id
        maker = "kuandeng"
        model = "pointgrey"
        projection_type = "perspective"
        sfm_camera = SfMCamera(camera_id=camera_id, maker=maker, model=model, projection_type=projection_type)
        #
        sfm_camera.k1 = camera_params.camera_distortion.k1
        sfm_camera.k1_prior = camera_params.camera_distortion.k1
        sfm_camera.k2 = camera_params.camera_distortion.k2
        sfm_camera.k2_prior = camera_params.camera_distortion.k2
        sfm_camera.k3 = camera_params.camera_distortion.k3
        sfm_camera.k3_prior = camera_params.camera_distortion.k3
        sfm_camera.p1 = camera_params.camera_distortion.p1
        sfm_camera.p1_prior = camera_params.camera_distortion.p1
        sfm_camera.p2 = camera_params.camera_distortion.p2
        sfm_camera.p2_prior = camera_params.camera_distortion.p2
        sfm_camera.focal_x = camera_params.focus_x
        sfm_camera.focal_y = camera_params.focus_y
        # image_dimensions[w, h]
        image_width, image_height = camera_params.image_dimensions
        #
        sfm_camera.focal_x_prior = camera_params.focus_x / image_width
        sfm_camera.focal_y_prior = camera_params.focus_y / image_height
        sfm_camera.cx = camera_params.principle_point_x
        sfm_camera.cy = camera_params.principle_point_y
        sfm_camera.cx_prior = camera_params.principle_point_x / image_width * 2
        sfm_camera.cy_prior = camera_params.principle_point_y / image_height * 2
        #
        focal_prior = camera_params.focus_x / image_width
        sfm_camera._focal = camera_params.focus_x
        sfm_camera._focal_prior = focal_prior
        #
        self._sfm_camera = sfm_camera

    def make_reference_lla(self):
        track_point_list = self._track.track_point_list
        if len(track_point_list) == 0:
            return
        center_x = 0
        center_y = 0
        center_z = 0
        # track_point = track_point_list[0]
        # if self._reverse:
        #     track_point = track_point_list[-1]
        for track_point in track_point_list:
            if not isinstance(track_point, TrackPoint):
                return
            center_x += track_point.coord.x
            center_y += track_point.coord.y
            center_z += track_point.coord.z
        track_point_count = 1.0 * len(track_point_list)
        center_x /= track_point_count
        center_y /= track_point_count
        center_z /= track_point_count
        reference_lla = {
            "latitude": center_y,
            "longitude": center_x,
            "altitude": center_z,
        }
        return reference_lla
