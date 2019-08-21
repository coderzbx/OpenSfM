# -*- coding:utf-8 -*-
from util import geo
from camera_info import SfMCamera
from track_info import Track


class Reconstruct:
    def __init__(self, camera, reference, track):
        self._camera = camera
        self._reference = reference
        self._track = track

    def reconstruct(self):
        if not isinstance(self._camera, SfMCamera):
            return
        if not isinstance(self._track, Track):
            return
        if not isinstance(self._reference, geo.TopocentricConverter):
            return
        reconstruct_data = []
        return reconstruct_data
