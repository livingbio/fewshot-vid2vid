import numpy as np
import dlib
import cv2
import argparse
import os
import glob
from utils.image_utility import save_image, generate_random_color, draw_border
from imutils import face_utils
import json


def dl_landmarks(image, gray, h, w, image_name_without_ext, output_dir):
    # This is based on SSD deep learning pretrained model

    # https://docs.opencv.org/trunk/d6/d0f/group__dnn.html#ga29f34df9376379a603acd8df581ac8d7
    inputBlob = cv2.dnn.blobFromImage(cv2.resize(
        image, (300, 300)), 1, (300, 300), (104, 177, 123))

    face_detector.setInput(inputBlob)
    detections = face_detector.forward()

    for i in range(0, detections.shape[2]):

        # Probability of prediction
        prediction_score = detections[0, 0, i, 2]
        if prediction_score < args.thresold:
            continue

        # Compute the (x, y)-coordinates of the bounding box for the object
        box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
        (x1, y1, x2, y2) = box.astype("int")

        # For better landmark detection
        y1, x2 = int(y1 * 1.15), int(x2 * 1.05)

        # Make the prediction and transfom it to numpy array
        shape = predictor(gray, dlib.rectangle(left=x1, top=y1, right=x2, bottom=y2))
        shape = face_utils.shape_to_np(shape)
        shape = shape.tolist()

        with open(os.path.join(output_dir, img_name_without_ext + ".json"), "w") as f:
            json.dump(shape, f)

        break


def face_detection(image, image_name_without_ext, output_dir):

    # Converting the image to gray scale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    img_height, img_width = image.shape[:2]
    dl_landmarks(image, gray, img_height, img_width, image_name_without_ext, output_dir)


if __name__ == "__main__":

    # Handle command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_dir', required=True, help='Input directory for the image')
    parser.add_argument('-w', '--weights',
                    default='./utils/shape_predictor_68_face_landmarks.dat', help='Facial Landmarks Model')
    parser.add_argument("-p", "--prototxt", default="./utils/deploy.prototxt.txt",
                    help="Caffe 'deploy' prototxt file")
    parser.add_argument("-m", "--model", default="./utils/res10_300x300_ssd_iter_140000.caffemodel",
                    help="Pre-trained caffe model")
    parser.add_argument("-t", "--thresold", type=float, default=0.6,
                    help="Thresold value to filter weak detections")
    parser.add_argument("-o", "--landmark_output_dir", default=".", help="Output directory for the landmarks")
    args = parser.parse_args()

    if not os.path.exists(args.landmark_output_dir):
        os.makedirs(args.landmark_output_dir, exist_ok=True)


    # Pre-trained caffe deep learning face detection model (SSD)
    face_detector = cv2.dnn.readNetFromCaffe(args.prototxt, args.model)

    # Landmark predictor
    predictor = dlib.shape_predictor(args.weights)

    # If image is valid or not
    image = None
    if args.input_dir:
        # Load input image
        if os.path.isfile(args.input_dir):
            img_name = args.input_dir
            image = cv2.imread(img_name)
            img_name_without_ext = img_name.split("/")[-1].split(".")[0]

            if image is None:
                print("Please provide image ...")
            else:
                print("Face detection for image")
                face_detection(image, img_name_without_ext, args.landmark_output_dir)

        elif os.path.isdir(args.input_dir):
            for img_name in sorted(glob.glob(os.path.join(args.input_dir, "*.jpg"))):
                image = cv2.imread(img_name)
                img_name_without_ext = img_name.split("/")[-1].split(".")[0]

                if image is None:
                    print("Please provide image ...")
                else:
                    print("Face detection for {}".format(img_name_without_ext + ".jpg"))
                    face_detection(image, img_name_without_ext, args.landmark_output_dir)

        else:
            raise FileNotFoundError("{} is not a valid directory/file path".format(args.input_dir))
