# -*- coding:utf-8 -*-
import os
import json

from defines import Device, Camera, CameraParams, CameraDistortion, CameraExtendInfo


class DeviceInfo(object):
    def __init__(self, device_path):
        self._device_path = device_path

    def parse_device(self):
        if not os.path.exists(self._device_path):
            return

        with open(self._device_path, "r") as f:
            result = json.load(f)
        if result is None:
            return

        device = Device()
        if "id" in result:
            device.device_id = str(result["id"])
        if "cameraCalibrationInfo" in result:
            camera = Camera()
            camera_calibration_info = result["cameraCalibrationInfo"]
            if "id" in camera_calibration_info:
                camera.device_id = device.device_id
            camera_params = CameraParams()
            if "focusX" in camera_calibration_info:
                camera_params.focus_x = float(camera_calibration_info["focusX"])
            if "focusY" in camera_calibration_info:
                camera_params.focus_y = float(camera_calibration_info["focusY"])
            if "principlePointX" in camera_calibration_info:
                camera_params.principle_point_x = float(camera_calibration_info["principlePointX"])
            if "principlePointY" in camera_calibration_info:
                camera_params.principle_point_y = float(camera_calibration_info["principlePointY"])
            camera_distortion = CameraDistortion()
            if "distortionK1" in camera_calibration_info:
                camera_distortion.k1 = float(camera_calibration_info["distortionK1"])
            if "distortionK2" in camera_calibration_info:
                camera_distortion.k2 = float(camera_calibration_info["distortionK2"])
            if "distortionK3" in camera_calibration_info:
                camera_distortion.k3 = float(camera_calibration_info["distortionK3"])
            if "distortionP1" in camera_calibration_info:
                camera_distortion.p1 = float(camera_calibration_info["distortionP1"])
            if "distortionP2" in camera_calibration_info:
                camera_distortion.p2 = float(camera_calibration_info["distortionP2"])
            camera_params.camera_distortion = camera_distortion

            image_w = 2448
            image_h = 2048
            if "imageWidth" in camera_calibration_info:
                image_w = int(camera_calibration_info["imageWidth"])
            if "imageHeight" in camera_calibration_info:
                image_h = int(camera_calibration_info["imageHeight"])
            camera_params.image_dimensions = [image_w, image_h]

            camera_param_map = {
                camera.device_id: camera_params
            }
            camera.camera_params = camera_param_map
            device.camera_map = {
                camera.device_id: camera
            }
        return device

    @staticmethod
    def get_camera_extend_info(extend_json_path):
        if not os.path.exists(extend_json_path):
            return

        with open(extend_json_path, "r") as f:
            json_data = json.load(f)
        if json_data is None:
            return

        camera_extend = CameraExtendInfo()
        if "cameraHeight" in json_data:
            camera_extend.camera_height = float(json_data["cameraHeight"])
        if "rollDelta" in json_data:
            camera_extend.roll_delta = float(json_data["rollDelta"])
        if "pitchDelta" in json_data:
            camera_extend.pitch_delta = float(json_data["pitchDelta"])
        if "azimuthDelta" in json_data:
            camera_extend.azimuth_delta = float(json_data["azimuthDelta"])
        return camera_extend
