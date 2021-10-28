MODEL=$1
DATASET=$2

for SPLIT in test train; do
  RAW=dataset/${DATASET}_raw/${SPLIT}
  LMDB=dataset/${DATASET}/${SPLIT}
  echo ${LMDB}
  cd src
  python build_lmdb.py --config configs/projects/${MODEL}/${DATASET}/ampO1.yaml --data_root ${RAW} --output_root ${LMDB} --overwrite
done