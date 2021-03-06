# -*- coding:utf-8 -*-
# make exif informations
import os
import json
import shutil
import numpy as np
import cv2
import multiprocessing
import time

# from exif import Image

from .defines import Track, TrackPoint
from .camera_info import SfMCamera
from .label import self_full_labels


class ImageInfo(object):
    def __init__(self, track, sfm_camera, track_data_dir, sfm_data_dir, combine_track=False, reverse_track=False):
        self._track = track
        self._sfm_camera = sfm_camera
        self._track_data_dir = track_data_dir
        self._sfm_data_dir = sfm_data_dir
        self._reverse_track = reverse_track
        self._id_track_point_map = {}
        self._track_point_timestamp_map = {}
        self._manager = multiprocessing.Manager()
        self._queue = self._manager.Queue()
        self._combine_track = combine_track

        self._init = True
        self._src_images_dir = os.path.join(self._track_data_dir, "src")
        if not os.path.exists(self._src_images_dir):
            self._init = False
            return

        self._seg_images_dir = os.path.join(self._track_data_dir, "seg")

        if not os.path.exists(self._sfm_data_dir):
            os.makedirs(self._sfm_data_dir)

        self._images_dir = os.path.join(self._sfm_data_dir, "images")
        if not os.path.exists(self._images_dir):
            os.makedirs(self._images_dir)

        self._masks_dir = os.path.join(self._sfm_data_dir, "masks")
        if os.path.exists(self._seg_images_dir):
            if not os.path.exists(self._masks_dir):
                os.makedirs(self._masks_dir)

        self._segmentations_dir = os.path.join(self._sfm_data_dir, "segmentations")
        if not os.path.exists(self._segmentations_dir):
            os.makedirs(self._segmentations_dir)

        self._exif_dir = os.path.join(self._sfm_data_dir, "exif")
        if not os.path.exists(self._exif_dir):
            os.makedirs(self._exif_dir)

    def format_images(self):
        if not self._init:
            return
        file_list = os.listdir(self._src_images_dir)
        src_image_list = []
        for file_name in file_list:
            if not file_name.endswith("jpg") and not file_name.endswith("jpeg"):
                continue
            src_image_list.append(file_name)
        #
        track_point_id_list = [track_point.track_point_id for track_point in self._track.track_point_list]
        track_point_timestamp_list = [track_point.loc_time for track_point in self._track.track_point_list]
        #
        cur_index = 0
        track_point_id_list.sort(reverse=self._reverse_track)
        #
        for track_point_id in track_point_id_list:
            self._track_point_timestamp_map[track_point_id] = track_point_timestamp_list[cur_index]
            cur_index += 1

        src_image_list.sort(reverse=self._reverse_track)
        #
        image_index = 0
        for image_name in src_image_list:
            track_point_id = image_name.split(".")[0]
            src_image_path = os.path.join(self._src_images_dir, image_name)
            #
            image_index += 1
            str_index = str(image_index).zfill(4)
            sfm_image_name = "{}.jpg".format(str_index)
            if self._combine_track:
                sfm_image_name = image_name
            sfm_image_path = os.path.join(self._images_dir, sfm_image_name)

            # copy
            shutil.copy(src=src_image_path, dst=sfm_image_path)
            #
            self._id_track_point_map[track_point_id] = sfm_image_name

    def make_exif(self, origin_pos_path):
        if not isinstance(self._track, Track):
            return
        if not isinstance(self._sfm_camera, SfMCamera):
            return
        track_point_list = self._track.track_point_list
        origin_pos_data = []
        for track_point in track_point_list:
            if not isinstance(track_point, TrackPoint):
                return
            track_point_id = track_point.track_point_id
            if track_point_id not in self._id_track_point_map:
                continue
            if track_point_id not in self._track_point_timestamp_map:
                continue
            time_stamp = self._track_point_timestamp_map[track_point_id]

            sfm_image_name = self._id_track_point_map[track_point_id]
            #
            c_matrix = np.matrix([[track_point.utm_coord.x], [track_point.utm_coord.y], [track_point.utm_coord.z]])
            r_matrix = np.matrix(track_point.R)
            t_matrix = r_matrix.dot(-c_matrix)
            #
            T_json = np.array(t_matrix).reshape(-1, ).tolist()
            R_list = np.array(r_matrix).reshape(-1, ).tolist()
            R_json = [
                [R_list[0], R_list[1], R_list[2]],
                [R_list[3], R_list[4], R_list[5]],
                [R_list[6], R_list[7], R_list[8]]
            ]
            lla_c = [track_point.coord.x, track_point.coord.y, track_point.coord.z]
            origin_pos = {
                sfm_image_name: {
                    "R": track_point.R,
                    "T": track_point.T,
                    "C": track_point.C
                }
            }
            origin_pos_data.append(origin_pos)
            exif_name = "{}.exif".format(sfm_image_name)
            exif_data = {
                "width": self._sfm_camera.width,
                "height": self._sfm_camera.height,
                "camera": str(self._sfm_camera.camera_id),
                "projection_type": self._sfm_camera.projection_type,
                "orientation": self._sfm_camera.orientation,
                "focal_ratio": self._sfm_camera.focal_prior,
                "make": self._sfm_camera.maker,
                "model": self._sfm_camera.model,
                "gps": {
                    "latitude": track_point.utm_coord.y,
                    "longitude": track_point.utm_coord.x,
                    "altitude": track_point.utm_coord.z,
                    "dop": 20.0,
                },
                # ms->s
                "capture_time": time_stamp / 1000,
                "gps_status": track_point.gps_status,
                "imu_status": track_point.imu_status,
                "r": track_point.R,
                "t": track_point.T,
                "c": track_point.C
            }
            # test
            r_matrix = np.matrix(exif_data['r'])
            R = np.array(r_matrix, dtype=float)
            [x, y, z] = exif_data['c']
            c_matrix = np.matrix([[x], [y], [z]])
            # c_matrix = np.matrix([[track_point.coord.x], [track_point.coord.y], [track_point.coord.z]])
            t_matrix = r_matrix.dot(-c_matrix)
            t = np.array(t_matrix)
            Rt = np.empty((3, 4))
            Rt[:, :3] = r_matrix
            Rt[:, 3] = [t[0][0], t[1][0], t[2][0]]

            exif_file_path = os.path.join(self._exif_dir, exif_name)
            with open(exif_file_path, "w") as f:
                json.dump(exif_data, f)

        with open(origin_pos_path, "w") as f:
            json.dump(origin_pos_data, f)

    def make_photo_info(self):
        photo_data_list = []
        if not isinstance(self._track, Track):
            return
        track_point_list = self._track.track_point_list
        for track_point in track_point_list:
            if not isinstance(track_point, TrackPoint):
                return
            track_point_id = track_point.track_point_id
            if track_point_id not in self._id_track_point_map:
                continue
            sfm_image_name = self._id_track_point_map[track_point_id]
            sfm_image_path = "/odm_data/images/" + sfm_image_name
            photo_data = {
                "filename": sfm_image_path,
                "latitude": track_point.utm_coord.y,
                "longitude": track_point.utm_coord.x,
                "altitude": track_point.utm_coord.z,
                "width": 2448,
                "height": 2048
            }
            photo_data_list.append(photo_data)
        photo_file_path = os.path.join(self._sfm_data_dir, "images.json")
        with open(photo_file_path, "w") as f:
            json.dump(photo_data_list, f)

    def convert_image_mask(self):
        while True:
            if self._queue.empty():
                break
            #
            start = time.time()
            src_seg_path = self._queue.get()
            file_name = os.path.basename(src_seg_path)
            track_point_id = file_name.split(".")[0]
            sfm_image_name = self._id_track_point_map[track_point_id]
            mask_name = "{}.png".format(sfm_image_name)
            mask_path = os.path.join(self._masks_dir, mask_name)
            segmentation_path = os.path.join(self._segmentations_dir, mask_name)
            #
            if os.path.exists(mask_path) and os.path.exists(segmentation_path):
                print("{} exists".format(mask_name))
                continue
            # convert png to id
            seg_image_mat = cv2.imread(src_seg_path)
            width = seg_image_mat.shape[1]
            height = seg_image_mat.shape[0]
            label_data = np.zeros((height, width), np.uint8)
            label_data[0:height, 0:width] = 255

            for label in self_full_labels:
                if label.categoryId != 0:
                    continue
                color = (label.color[2], label.color[1], label.color[0])
                category_id = label.categoryId
                label_data[np.where((seg_image_mat == color).all(axis=2))] = category_id
            #
            cv2.imwrite(mask_path, label_data)
            cv2.imwrite(segmentation_path, label_data)

            end = time.time()
            print("Processed {} in {} ms".format(mask_name, str((end - start) * 1000)))

    def make_mask_images(self, cpu_num=16):
        if not os.path.exists(self._masks_dir):
            return

        file_list = os.listdir(self._seg_images_dir)
        for file_name in file_list:
            if not file_name.endswith("png"):
                continue

            src_seg_path = os.path.join(self._seg_images_dir, file_name)
            self._queue.put(src_seg_path)

        self_threads = []
        for i in range(cpu_num):
            t = multiprocessing.Process(target=self.convert_image_mask)
            t.daemon = True
            self_threads.append(t)

        for process in self_threads:
            process.start()

        for process in self_threads:
            process.join()
