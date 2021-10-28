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

rm projects/*/*.tar.gz
rm projects/*/test_data -rf

cmd="python download_test_data.py --model_name fs_vid2vid"
output

CONFIG=configs/projects/fs_vid2vid/face_forensics/ampO1.yaml
if test -f "$CONFIG"; then
  cmd="python inference.py --single_gpu --num_workers 0 \
  --config $CONFIG \
  --output_dir projects/fs_vid2vid/output/face_forensics"
  output
fi