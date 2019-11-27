# -*- coding:utf-8 -*-
import os
import argparse

import json

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--reconstruction", type=str, required=True)
    parser.add_argument("--ply", type=str, required=True)
    params = parser.parse_args()

    reconstruction_path = params.reconstruction
    ply_path = params.ply

    if not os.path.exists(reconstruction_path):
        exit(-1)

    output_dir = os.path.dirname(ply_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    reconstruction_data = json.load(open(reconstruction_path, "r"))
    reconstruction_count = len(reconstruction_data)
    reconstruction = reconstruction_data[0]
    if "points" not in reconstruction:
        exit(0)

    points_data = reconstruction["points"]
    point_count = len(points_data)
    f = open(ply_path, "w")
    ply_header = \
        "ply\n" \
        "format ascii 1.0\n" \
        "element vertex {}\n"\
        "property double x\n" \
        "property double y\n" \
        "property double z\n" \
        "property float nx\n" \
        "property float ny\n" \
        "property float nz\n" \
        "property uchar diffuse_red\n" \
        "property uchar diffuse_green\n" \
        "property uchar diffuse_blue\n" \
        "property uchar class\n" \
        "property uchar detection\n" \
        "end_header\n".format(point_count)
    f.write(ply_header)

    for _, point_info in points_data.items():
        print("point_id:", _)
        r, g, b = point_info["color"]
        x, y, z = point_info["coordinates"]
        ply_data = "{:.8f} {:.8f} {:.8f} {:.3f} {:.3f} {:.3f} {} {} {} {} {}\n".format(
            x, y, z, 0, 0, 0, int(r), int(g), int(b), 0, 0
        )
        f.write(ply_data)
    f.close()
