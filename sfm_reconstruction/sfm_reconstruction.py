# -*- coding:utf-8 -*-
import os
import sys
import json
import shutil
import time

from sfm_data_maker.track_info import TrackInfo
from sfm_data_maker.camera_info import SfMCamera
from sfm_data_maker.image_info import ImageInfo
from sfm_data_maker.config import Config


class TaskInfo:
    def __init__(self):
        self.feature_type = "SIFT"
        self.cpu_num = 20
        self.track_id = ""
        self.input_root_path = ""
        self.output_root_path = ""
        self.src_image_path = ""
        self.track_json_path = ""
        self.ground_recognition_path = ""


def parse_input_json(file_path):
    if not os.path.exists(file_path):
        return None
    task_info = TaskInfo()
    with open(file_path) as f:
        json_data = json.load(f)
    if json_data is None:
        return None

    input_data = json_data["input"]
    params_data = input_data["params"]
    for param_info in params_data:
        k = param_info["k"]
        v = param_info["v"]
        if k == "trackIds":
            task_info.track_id = v
        elif k == "featureType":
            task_info.feature_type = v
        elif k == "cpuNums":
            task_info.cpu_num = int(v)
            if task_info.cpu_num <= 0:
                task_info.cpu_num = 20
    # check track_id
    if len(task_info.track_id) == 0:
        print("parse trackId failed: ", task_info.track_id)
        return None
    task_info.input_root_path = input_data["rootPath"]
    if not os.path.exists(task_info.input_root_path):
        print("input root path is not exists: ", task_info.input_root_path)
        return None
    types_data = input_data["types"]
    for type_data in types_data:
        file_name = type_data["fileName"]
        dir_path = os.path.join(task_info.input_root_path, file_name)
        type_name = type_data["type"]
        if type_name == "source_image":
            task_info.src_image_path = dir_path
        elif type_name == "ground_recognition":
            task_info.ground_recognition_path = dir_path
        elif type_name == "track_all":
            task_info.track_json_path = dir_path
    # output
    output_data = json_data["output"]
    task_info.output_root_path = output_data["rootPath"]
    return task_info


if __name__ == "__main__":
    argc_count = len(sys.argv)
    if argc_count <= 1:
        print("parameter[1] must be input json")
        exit(-1)
    # check input json
    input_json = sys.argv[1]
    if not os.path.exists(input_json):
        print("input json is not exists: ", input_json)
        exit(-1)
    # parse input json
    task_info_ = parse_input_json(input_json)
    if task_info_ is None:
        print("parse input json failed")
        exit(-1)
    # format workspace
    src_image_path = os.path.join(task_info_.src_image_path, task_info_.track_id)
    recognition_path = os.path.join(task_info_.ground_recognition_path, task_info_.track_id)
    track_json_path = os.path.join(task_info_.track_json_path, task_info_.track_id, "track_all.json")

    workspace_dir = os.path.join(task_info_.input_root_path, "sfm_reconstruction_workspace")
    if os.path.exists(workspace_dir):
        file_list = os.listdir(workspace_dir)
        for file_id in file_list:
            file_path = os.path.join(workspace_dir, file_id)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.remove(file_path)
    if not os.path.exists(workspace_dir):
        os.makedirs(workspace_dir)
    # move data
    workspace_seg_dir = os.path.join(workspace_dir, "seg")
    workspace_src_dir = os.path.join(workspace_dir, "src")
    os.symlink(src_image_path, workspace_src_dir)
    os.symlink(recognition_path, workspace_seg_dir)
    # format json
    with open(track_json_path) as f:
        track_json_data = json.load(f)
        #
        track_json_file = os.path.join(workspace_dir, "track.json")
        shutil.copy(track_json_path, os.path.join(workspace_dir, "track.json"))
        #
        device_json_file = os.path.join(workspace_dir, "device.json")
        device_data = track_json_data["deviceInfo"]
        with open(device_json_file, "w") as f1:
            json.dump(device_data, f1)
        #
        extend_json_file = os.path.join(workspace_dir, "trackExtend.json")
        extend_data = track_json_data["camera_height"]
        with open(extend_json_file, "w") as f2:
            json.dump(extend_data, f2)
    # create task info
    task_info_path = os.path.join(workspace_dir, "task_info.json")
    task_json_data = {
        "track_id": task_info_.track_id,
        "output_root_path": task_info_.output_root_path
    }
    with open(task_info_path, "w") as f:
        json.dump(task_json_data, f)
    # create output path file
    with open("/source/OpenSfM/output_dir.txt", "w") as f:
        f.write(workspace_dir)
    # create data for reconstruction
    # parse device => get camera
    track_handler = TrackInfo(workspace_dir=workspace_dir,
                              track_json_path=os.path.join(workspace_dir, "track.json"),
                              track_id=task_info_.track_id)
    track_handler.parse_track(track_json_path=os.path.join(workspace_dir, "track.json"))
    track_handler.parse_device(device_path=os.path.join(workspace_dir, "device.json"))
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
    camera_model_path = os.path.join(workspace_dir, "camera_models.json")
    with open(camera_model_path, "w") as f:
        json.dump(camera_model_data, f)
    print("make camera_models.json succeed")
    print("making exif and format images...")
    track_data_dir = os.path.join(workspace_dir)
    image_info = ImageInfo(track=track_handler.track, sfm_camera=track_handler.sfm_camera,
                           track_data_dir=workspace_dir, sfm_data_dir=workspace_dir)
    image_info.format_images()
    # save origin_pos
    origin_pos_path = os.path.join(task_info_.output_root_path, task_info_.track_id)
    image_info.make_exif(origin_pos_path=origin_pos_path)
    image_info.make_mask_images(cpu_num=task_info_.cpu_num)
    print("make exif succeed")
    #
    print("making config.yaml...")
    feature_type = task_info_.feature_type
    config_handler = Config(feature_type=feature_type)
    yaml_data = config_handler.make_config_yaml()
    config_yaml_path = os.path.join(workspace_dir, "config.yaml")
    with open(config_yaml_path, "w") as f:
        for config_data in yaml_data:
            f.write("{}\n".format(config_data))
    print("make config.yaml succeed")
    time2 = time.time()
    print("format workspace directory done in {} s".format(time2 - time1))

    exit(0)
