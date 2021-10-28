FROM nvidia/cuda:11.1.1-cudnn8-devel-ubuntu20.04

ENTRYPOINT []

COPY ./src /work/src
COPY ./scripts /work/scripts
WORKDIR /work
RUN ./scripts/install.sh

COPY ./requirements.txt /requirements.txt
RUN pip3 install --ignore-installed --upgrade -r /requirements.txt

RUN ./scripts/test_inference.sh
RUN ./scripts/test_training.sh

WORKDIR /work/src