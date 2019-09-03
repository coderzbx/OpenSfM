# -*- coding:utf-8 -*-
from enum import Enum


class FeatureType(Enum):
    AKAZE = 0,
    SURF = 1,
    SIFT = 2,
    HAHOG = 3,
    ORB = 4


class SIFT_Params(object):
    def __init__(self, sift_peak_threshold=0.1, sift_edge_threshold=10):
        # Smaller value -> more features
        self._sift_peak_threshold = sift_peak_threshold
        self._sift_edge_threshold = sift_edge_threshold

    def format_params(self):
        params_data = {
            "sift_peak_threshold": self._sift_peak_threshold,
            "sift_edge_threshold": self._sift_edge_threshold
        }
        return params_data


class GPSAlignmentParams(object):
    def __init__(self, use_altitude_tag=True, align_method="orientation_prior",
                 align_orientation_prior="horizontal", bundle_use_gps=True, bundle_use_gcp=False):
        # Use or ignore EXIF altitude tag
        self._use_altitude_tag = "yes"
        if not use_altitude_tag:
            self._use_altitude_tag = "no"
        # orientation_prior or naive
        self._align_method = align_method
        # horizontal, vertical or no_roll
        self._align_orientation_prior = align_orientation_prior
        # Enforce GPS position in bundle adjustment
        self._bundle_use_gps = "yes"
        if not bundle_use_gps:
            self._bundle_use_gps = "no"
        # Enforce Ground Control Point position in bundle adjustment
        self._bundle_use_gcp = "yes"
        if not bundle_use_gcp:
            self._bundle_use_gcp = "no"

    def format_params(self):
        params_data = {
            "use_altitude_tag": self._use_altitude_tag,
            "align_method": self._align_method,
            "align_orientation_prior": self._align_orientation_prior,
            "bundle_use_gps": self._bundle_use_gps,
            "bundle_use_gcp": self._bundle_use_gcp
        }
        return params_data


class PreemptiveMatchingParams(object):
    def __init__(self, matching_gps_distance=0, matching_gps_neighbors=0, matching_time_neighbors=0,
                 matching_order_neighbors=10, matching_bow_neighbors=0):
        # Maximum gps distance between two images for matching
        self._matching_gps_distance = matching_gps_distance
        # Number of images to match selected by GPS distance. Set to 0 to use no limit (or disable if matching_gps_distance is also 0)
        self._matching_gps_neighbors = matching_gps_neighbors
        # Number of images to match selected by time taken. Set to 0 to disable
        self._matching_time_neighbors = matching_time_neighbors
        # Number of images to match selected by image name. Set to 0 to disable
        self._matching_order_neighbors = matching_order_neighbors
        # Number of images to match selected by BoW distance. Set to 0 to disable
        self._matching_bow_neighbors = matching_bow_neighbors

    def format_params(self):
        params_data = {
            "matching_gps_distance": self._matching_gps_distance,
            "matching_gps_neighbors": self._matching_gps_neighbors,
            "matching_time_neighbors": self._matching_time_neighbors,
            "matching_order_neighbors": self._matching_order_neighbors,
            "matching_bow_neighbors": self._matching_bow_neighbors
        }
        return params_data


class Config(object):
    def __init__(self, processes=16, feature_type="HAHOG", feature_root=1, feature_min_frames=2000,
                 feature_process_size=-1, feature_use_adaptive_suppression=False):
        # processes
        self._processes = processes
        # Feature type (AKAZE, SURF, SIFT, HAHOG, ORB)
        self._feature_type = feature_type
        # If 1, apply square root mapping to features
        self._feature_root = feature_root
        # If fewer frames are detected, sift_peak_threshold/surf_hessian_threshold is reduced.
        self._feature_min_frames = feature_min_frames
        # Resize the image if its size is larger than specified. Set to -1 for original size
        self._feature_process_size = feature_process_size
        self._feature_use_adaptive_suppression = feature_use_adaptive_suppression

    def format_params(self):
        params_data = {
            "processes": self._processes,
            "feature_type": self._feature_type,
            "feature_root": self._feature_root,
            "feature_min_frames": self._feature_min_frames,
            "feature_process_size": self._feature_process_size,
            "feature_use_adaptive_suppression": self._feature_use_adaptive_suppression,
            "segmentation_ignore_values": [0],
            "optimize_camera_parameters": False
        }
        return params_data

    def make_config_yaml(self):
        yaml_data = []
        all_config_class = [SIFT_Params, GPSAlignmentParams, PreemptiveMatchingParams]
        for class_instance in all_config_class:
            config_instance = class_instance()
            params_data = config_instance.format_params()
            for k, v in params_data.items():
                yaml_config = "{}: {}".format(k, v)
                yaml_data.append(yaml_config)
        params_data = self.format_params()
        for k, v in params_data.items():
            yaml_config = "{}: {}".format(k, v)
            yaml_data.append(yaml_config)
        return yaml_data
