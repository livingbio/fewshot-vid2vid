VIDEO_PATH=projects/fs_vid2vid/data/videos/00000.mp4
IMG_DIR=projects/fs_vid2vid/data/images/00000
LANDMARK_DIR=projects/fs_vid2vid/data/landmarks-dlib68/00000

cd src
python video_to_frames.py -i $VIDEO_PATH -o $IMG_DIR
python facial_landmarks.py -i $IMG_DIR -o $LANDMARK_DIR