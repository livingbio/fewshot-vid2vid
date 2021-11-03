#!/bin/sh
CURRENT=$(pwd)

# Check CUDA_VERSION
export CUDA_VERSION=$(nvcc --version| grep -Po "(\d+\.)+\d+" | head -1)
export TORCH_CUDA_ARCH_LIST="5.2;5.3;6.0;6.1;6.2;7.0;7.2;7.5;8.0;8.6+PTX"

apt update -y && \
    apt install python3 python3-pip git -y && \
    rm -rf /var/lib/apt/lists/*

ln -s /usr/bin/python3 /usr/bin/python

apt update -y && DEBIAN_FRONTEND=noninteractive apt install -y --allow-downgrades --allow-change-held-packages --no-install-recommends \
    build-essential \
    cmake \
    git \
    curl \
    vim \
    tmux \
    wget \
    bzip2 \
    unzip \
    g++ \
    ca-certificates \
    ffmpeg \
    libx264-dev \
    imagemagick \
    libnss3-dev \
    ninja-build

pip3 install torch==1.9.1+cu111 torchvision==0.10.1+cu111 torchaudio==0.9.1 -f https://download.pytorch.org/whl/cu111/torch_stable.html
pip3 install --ignore-installed --upgrade -r requirements.txt

for p in correlation channelnorm resample2d bias_act upfirdn2d; do
      cd ./src/imaginaire/third_party/${p};
      rm -rf build dist *info;
      python3 setup.py install;
      cd ${CURRENT};
done

for p in gancraft/voxlib; do
      cd ./src/imaginaire/model_utils/${p};
      make all
      cd ${CURRENT};
done