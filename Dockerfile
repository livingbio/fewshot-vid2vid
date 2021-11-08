FROM pytorch/pytorch:1.9.0-cuda11.1-cudnn8-devel

ENTRYPOINT []

COPY ./src /work/src
COPY ./scripts /work/scripts
COPY ./requirements.txt /work/requirements.txt

WORKDIR /work
RUN ./scripts/install.sh

WORKDIR /work/src