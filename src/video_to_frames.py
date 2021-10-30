import cv2
import time
import os
import argparse

def video_to_frames(input_loc, output_loc):
    """Function to extract frames from input video file
    and save them as separate frames in an output directory.
    Args:
        input_loc: Input video file.
        output_loc: Output directory to save the frames.
    Returns:
        None
    """
    try:
        os.mkdir(output_loc)
    except OSError:
        pass

    # Log the time
    time_start = time.time()

    # Start capturing the feed
    cap = cv2.VideoCapture(input_loc)

    # Find the number of frames
    video_length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) - 1
    print ("Number of frames: ", video_length)
    count = 0
    print ("Converting video..\n")

    # Start converting the video
    while cap.isOpened():
        # Extract the frame
        ret, frame = cap.read()

        if not ret:
            continue

        # Write the results back to output location.
        cv2.imwrite(output_loc + "/%#05d.jpg" % (count+1), frame)
        count = count + 1

        # If there are no more frames left
        if (count > (video_length-1)):
            # Log the time again
            time_end = time.time()

            # Release the feed
            cap.release()

            # Print stats
            print ("Done extracting frames.\n%d frames extracted" % count)
            print ("It took %d seconds for conversion." % (time_end-time_start))
            break

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_file", required=True, help="Path to the input video file")
    parser.add_argument("-o", "--output_dir", required=True, help="Path to the output directory")

    args = parser.parse_args()

    if not os.path.isfile(args.input_file):
        raise FileNotFoundError("{} is not a valid file path".format(args.input_file))

    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir, exist_ok=True)

    video_to_frames(args.input_file, args.output_dir)