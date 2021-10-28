#!/bin/bash
function output {
  eval ${cmd}
  RESULT=$?
  if [ $RESULT -eq 0 ]; then
    echo -e "\e[1;32m ${cmd} [Success] \e[0m"
  else
    echo -e "\e[1;31m ${cmd} [Failure] \e[0m"
    exit 1
  fi
}

cd src

LOG="/tmp/unit_test.log"
BASE_CMD="python -m torch.distributed.launch --nproc_per_node=1 train.py "

CONFIG=configs/unit_test/fs_vid2vid_face.yaml
if test -f "$CONFIG"; then
  cmd="${BASE_CMD} --config $CONFIG >> ${LOG} "
  output
fi

CONFIG=configs/unit_test/fs_vid2vid_pose.yaml
if test -f "$CONFIG"; then
  cmd="${BASE_CMD} --config $CONFIG >> ${LOG} "
  output
fi
