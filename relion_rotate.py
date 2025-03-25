#!/usr/bin/env python3
#
# Author: Jiaqiang Qian, assisted by GPT, Claude, & Gemini, 2025 @FDU, MIT License
#
# VirtualIce: Half-synthetic CryoEM Micrograph Generator
#
# This script generates half-synthetic cryoEM micrographs given protein structures and a list
# of noise micrographs and their defoci. It is intended that the noise micrographs are cryoEM
# images of buffer and that the junk & substrate are masked out using AnyLabeling.
#

import sys
import numpy as np
import pandas as pd
import mrcfile
from scipy.spatial.transform import Rotation as R
from starparser import fileparser

# https://www.ccpem.ac.uk/docs/euler-angle-conventions/
# RELION | ZYZ. Conventions are the same as in XMIPP and FREALIGN

def uniform_sample(n):
    return np.round(R.random(n).as_euler("zyz", degrees=True), 3)


def rotate_z_sample(n, var=10):
    "ZYZ"
    alpha = np.round(np.random.uniform(0, 360, n), 3)
    beta = np.round(np.random.normal(0, var / 2, n), 3)
    beta += np.round(np.random.choice([0,180], n, replace=True), 3)
    beta = np.round(beta,3)
    gamma = np.round(np.random.uniform(0, 360, n), 3)
    return np.array([alpha, beta, gamma]).T

# default
# [* , -90/90, *]
# for emd 38776
# [-45 ,-20/160,*]
# for emd_6336
# [-45, -90/90, *]
def rotate_xy_plane(n, var=10):
    "ZYZ"
    alpha = np.round(np.random.uniform(0, 360, n), 3)
    #alpha += np.round(np.random.normal(0, var / 2, n), 3)

    #gamma = np.round(np.random.normal(0, var / 2, n), 3)
    beta  = np.round(np.random.choice([-90.0,90.0], n, replace=True), 3)
    beta += np.round(np.random.normal(0, var / 2, n), 3)
    beta = np.round(beta,3)
    test = 0

    gamma = np.round(np.random.uniform(0, 360, n), 3)
    #gamma  = np.round(np.random.choice([0.0], n, replace=True), 3)
    return np.array([alpha, beta, gamma]).T


def write_rotate_star(particle, star_file_path):
    relion_version = ["#", "version", "30001"]
    relion_optics = [
        "_rlnVoltage",
        "_rlnImagePixelSize",
        "_rlnSphericalAberration",
        "_rlnAmplitudeContrast",
        "_rlnOpticsGroup",
        "_rlnImageSize",
        "_rlnImageDimensionality",
        "_rlnOpticsGroupName",
    ]

    relion_optics_data = {
        "_rlnVoltage": "300.0",
        "_rlnImagePixelSize": "1.22",
        "_rlnSphericalAberration": "2.7",
        "_rlnAmplitudeContrast": "0.1",
        "_rlnOpticsGroup": "1",
        "_rlnImageSize": "256",
        "_rlnImageDimensionality": "2",
        "_rlnOpticsGroupName": "OpticsGroup1",
    }
    print(type(relion_optics_data))
    relion_data_columns = ["_rlnAngleRot", "_rlnAngleTilt", "_rlnAnglePsi"]
    relion_star_data = pd.DataFrame(particle, columns=relion_data_columns)

    relion_star_metadata = [
        relion_version,
        relion_optics,
        pd.DataFrame.from_dict(relion_optics_data,orient="index").T,
        #pd.DataFrame.from_dict(relion_optics_data,orient="columns", columns=relion_optics),
        relion_data_columns,
        "data_particles",
    ]
    print(relion_star_metadata)
    fileparser.writestar(relion_star_data, relion_star_metadata, star_file_path)


def run_mem(N ,p1=0.4, p2=0.4, p3=0.2):
    "rotate z 40%; rotate xy plane 40%; random 20%"

    particle_z = rotate_z_sample(np.int32(N * p1))
    particle_xy = rotate_xy_plane(np.int32(N * p2))
    particle_uni = uniform_sample(np.int32(N * p3))

    particle = np.concatenate((particle_z, particle_xy, particle_uni), axis=0)

    write_rotate_star(particle, "rotate_64.star")

def run_protein(N):
    particle_uni = uniform_sample(N)
    write_rotate_star(particle_uni, "rotate_uni.star")

if __name__ == "__main__":
    N = sys.argv[1]
    mrc = sys.argv[2]
    mode = sys.argv[3]

    f_mrc = mrcfile.open(mrc, mode="r+")
    # https://www.ccpem.ac.uk/mrc-format/mrc2014/
    # mapc mapr maps , 1 for X,2 for Y ,3 for Z
    rotate_mode = "XYZ"
    permute = (f_mrc.header["mapc"] -1 , f_mrc.header["mapr"]-1, f_mrc.header["maps"]-1)
    print(f"Check the axis of {mrc}.")
    match permute:
        case (0,1,2):
            print(f"mapc,mapr,maps of {mrc} is XYZ!")
            rotate_mode = "XYZ"
        case (2,1,0):
            print(f"mapc,mapr,maps of {mrc} is ZYX!")
            rotate_mode = "ZYX"
        case (1,2,0):
            print(f"mapc,mapr,maps of {mrc} is YZX!")
            rotate_mode = "YZX"

    if permute != (0,1,2):
        permute_data = f_mrc.data
        permute_data = np.transpose(permute_data,permute)
        f_mrc.set_data(permute_data)
        f_mrc.header["mapc"]=1
        f_mrc.header["mapr"]=2
        f_mrc.header["maps"]=3
        print(f"{mrc} is {permute} mode, transpose it to XYZ!")
    else:
        print(f"{mrc} is XYZ mode, no need to be transposed.")

    f_mrc.close()

    match mode:
        case "mem":
            run_mem(int(N))
        case "uni":
            run_protein(int(N))
        case _:
            raise NotImplementedError("membrane(mem)/ normal protein(uni) is allowed")
