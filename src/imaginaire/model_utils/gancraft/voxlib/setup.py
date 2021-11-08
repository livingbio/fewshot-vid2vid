# Copyright (C) 2021 NVIDIA CORPORATION & AFFILIATES.  All rights reserved.
#
# This work is made available under the Nvidia Source Code License-NC.
# To view a copy of this license, check out LICENSE.md
from setuptools import setup
from torch.utils.cpp_extension import BuildExtension, CUDAExtension
import os

cxx_args = list()
cxx_args.append('-fopenmp')
cxx_args.append('-Wall')
cxx_args.append('-std=c++14')

cuda_version = os.getenv('CUDA_VERSION')
print('CUDA_VERSION: {}'.format(cuda_version))

nvcc_args = list()
nvcc_args.append('-gencode')
nvcc_args.append('arch=compute_70,code=sm_70')
nvcc_args.append('-gencode')
nvcc_args.append('arch=compute_75,code=sm_75')
if cuda_version is not None:
    if cuda_version >= '11.0':
        nvcc_args.append('-gencode')
        nvcc_args.append('arch=compute_80,code=sm_80')
nvcc_args.append('-Xcompiler')
nvcc_args.append('-Wall')
nvcc_args.append('-std=c++14')

setup(
    name='voxrender',
    ext_modules=[
        CUDAExtension('voxlib', [
            'voxlib.cpp',
            'ray_voxel_intersection.cu',
            'sp_trilinear_worldcoord_kernel.cu',
            'positional_encoding_kernel.cu'
        ],
            extra_compile_args={'cxx': cxx_args, 'nvcc': nvcc_args}
        )
    ],
    cmdclass={
        'build_ext': BuildExtension
    })
