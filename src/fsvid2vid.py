import os
import shutil
import subprocess
from pathlib import Path
from tempfile import gettempdir

TEST_DATA_DIR = "projects/fs_vid2vid/test_data/faceForensics"


def preprocess(image_path, video_path):
    temp_dir = gettempdir()

    video_filename = Path(video_path).stem
    image_filename = Path(image_path).stem
    video_frame_dir = os.path.join(temp_dir, video_filename, "frames")
    video_landmark_dir = os.path.join(temp_dir, video_filename, "landmarks")

    # Generate frames for the video
    subprocess.run(
        [
            "python",
            "./utils/video_to_frames.py",
            "-i",
            video_path,
            "-o",
            video_frame_dir,
        ]
    )
    # Generate landmarks for the video frames
    subprocess.run(
        [
            "python",
            "./utils/facial_landmarks.py",
            "-i",
            video_frame_dir,
            "-o",
            video_landmark_dir,
        ]
    )
    # Generate landmarks for the reference image
    subprocess.run(
        ["python", "./utils/facial_landmarks.py", "-i", image_path, "-o", temp_dir]
    )

    shutil.rmtree(TEST_DATA_DIR)

    # Copy driving video files to destination folders
    video_frame_dest = os.path.join(TEST_DATA_DIR, "driving", "images")
    video_landmark_dest = os.path.join(TEST_DATA_DIR, "driving", "landmarks-dlib68")
    shutil.copytree(video_frame_dir, video_frame_dest)
    shutil.copytree(video_landmark_dir, video_landmark_dest)

    # Copy reference image files to destination folders
    image_frame_dest = os.path.join(TEST_DATA_DIR, "reference", "images")
    image_landmark_dest = os.path.join(TEST_DATA_DIR, "reference", "landmarks-dlib68")
    os.makedirs(image_frame_dest, exist_ok=True)
    os.makedirs(image_landmark_dest, exist_ok=True)
    shutil.copy(image_path, os.path.join(image_frame_dest, image_filename, ".jpg"))
    shutil.copy(
        image_filename + ".json",
        os.path.join(image_frame_dest, image_filename + ".json"),
    )


def inference(image_path, video_path):
    preprocess(image_path, video_path)
    subprocess.run(
        [
            "python",
            "inference.py",
            "--single_gpu",
            "--num_worker",
            "0",
            "--config",
            "configs/projects/fs_vid2vid/face_forensics/ampO1.yaml",
            "--output_dir",
            "projects/fs_vid2vid/output/face_forensics",
        ]
    )
