import os
import shutil
import subprocess
from pathlib import Path

output_path = "projects/fs_vid2vid/output/face_forensics"


def preprocess(image_path, video_path):
    test_data_dir = "projects/fs_vid2vid/test_data/faceForensics"

    video_filename, video_parent = Path(video_path).stem, Path(video_path).parent
    image_filename, image_parent = Path(image_path).stem, Path(image_path).parent
    video_frame_dir = os.path.join(video_parent, video_filename, "frames")
    video_landmark_dir = os.path.join(video_parent, video_filename, "landmarks")

    # Generate frames for the video and save them to temporary video frame directory
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
    # Generate landmarks for the video frames and save them to temporary video landmark directory
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
    # Generate landmarks (single image) for the reference image and save them temporary directory
    subprocess.run(
        ["python", "./utils/facial_landmarks.py", "-i", image_path, "-o", image_parent]
    )

    if os.path.isdir(test_data_dir):
        shutil.rmtree(test_data_dir)

    # Copy driving video files to destination folders
    video_frame_dest = os.path.join(test_data_dir, "driving", "images")
    video_landmark_dest = os.path.join(test_data_dir, "driving", "landmarks-dlib68")
    shutil.copytree(video_frame_dir, video_frame_dest)
    shutil.copytree(video_landmark_dir, video_landmark_dest)

    # Copy reference image files to destination folders
    image_frame_dest = os.path.join(test_data_dir, "reference", "images")
    image_landmark_dest = os.path.join(test_data_dir, "reference", "landmarks-dlib68")
    os.makedirs(image_frame_dest, exist_ok=True)
    os.makedirs(image_landmark_dest, exist_ok=True)
    shutil.copy(image_path, os.path.join(image_frame_dest, image_filename + ".jpg"))
    shutil.copy(
        os.path.join(image_parent, image_filename + ".json"),
        os.path.join(image_landmark_dest, image_filename + ".json"),
    )


def inference(image_path, video_path):
    preprocess(image_path, video_path)
    config_path = "configs/projects/fs_vid2vid/face_forensics/ampO1.yaml"
    subprocess.run(
        [
            "python",
            "inference.py",
            "--single_gpu",
            "--num_worker",
            "0",
            "--config",
            config_path,
            "--output_dir",
            output_path,
        ]
    )
