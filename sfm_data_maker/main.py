# -*- coding:utf-8 -*-
import os
import argparse
import time
import json

from track_info import TrackInfo
from camera_info import SfMCamera
from image_info import ImageInfo
from config import Config
from util import geo
from reconstruct import Reconstruct

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_set', type=str, required=False, default="kd")
    parser.add_argument('--track_dir', type=str, required=True)
    parser.add_argument('--track_id', type=str, required=True)
    parser.add_argument('--reverse_track', type=bool, required=False, default=False)
    params = parser.parse_args()

    data_set_name = params.data_set
    track_dir = params.track_dir
    track_id = params.track_id

    data_set_dir_name = "{}_{}".format(data_set_name, track_id)
    data_set_dir = os.path.join(track_dir, data_set_dir_name)
    if not os.path.exists(data_set_dir):
        os.makedirs(data_set_dir)

    # parse device => get camera
    track_handler = TrackInfo(track_dir=track_dir, track_id=track_id, reverse=params.reverse_track)
    track_handler.parse_track()
    track_handler.parse_device()
    #
    sfm_camera = track_handler.sfm_camera
    if not isinstance(sfm_camera, SfMCamera):
        print("device parse failed")
        exit(-1)

    #
    time1 = time.time()
    #
    print("making camera_models.json....")
    camera_model_data = sfm_camera.make_camera_model()
    camera_model_path = os.path.join(data_set_dir, "camera_models.json")
    with open(camera_model_path, "w") as f:
        json.dump(camera_model_data, f)
    print("make camera_models.json succeed")
    #
    print("making reference_lla.json...")
    reference_lla_data = track_handler.make_reference_lla()
    reference_lla_path = os.path.join(data_set_dir, "reference_lla.json")
    with open(reference_lla_path, "w") as f:
        json.dump(reference_lla_data, f)
    latitude = reference_lla_data["latitude"]
    longitude = reference_lla_data["longitude"]
    altitude = reference_lla_data["altitude"]
    reference_handler = geo.TopocentricConverter(reflat=latitude, reflon=longitude, refalt=altitude)
    print("make reference_lla.json succeed")
    #
    print("making exif and format images...")
    track_dir_name = "test_{}".format(track_id)
    track_data_dir = os.path.join(track_dir, track_dir_name)
    image_info = ImageInfo(track=track_handler.track, sfm_camera=track_handler.sfm_camera,
                           track_data_dir=track_data_dir, sfm_data_dir=data_set_dir,
                           reverse_track=params.reverse_track)
    image_info.format_images()
    image_info.make_exif()
    image_info.make_photo_info()
    print("make exif succeed")
    #
    print("making config.yaml...")
    config_handler = Config()
    yaml_data = config_handler.make_config_yaml()
    config_yaml_path = os.path.join(data_set_dir, "config.yaml")
    with open(config_yaml_path, "w") as f:
        for config_data in yaml_data:
            f.write("{}\n".format(config_data))
    print("make config.yaml succeed")
    #
    print("making reconstruct.json")
    reconstruct_handler = Reconstruct(camera=sfm_camera, reference=reference_handler, track=track_handler.track)
    print("reconstruct succeed")
    #
    time2 = time.time()
    print("works done in {} s".format(time2 - time1))
