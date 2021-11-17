FROM nvidia/cuda:11.1.1-cudnn8-devel-ubuntu20.04

ENTRYPOINT []

COPY ./src /work/src
COPY ./scripts /work/scripts
COPY ./requirements.txt /work/requirements.txt

WORKDIR /work
#RUN ./scripts/install.sh

WORKDIR /work/src