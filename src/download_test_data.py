import argparse
import os
import sys
import tarfile

from imaginaire.utils.io import download_file_from_google_drive  # noqa: E402

URLS = {
    'fs_vid2vid': '1fTj0HHjzcitgsSeG5O_aWMF8yvCQUQkN',
}


def parse_args():
    parser = argparse.ArgumentParser(description='Download test data.')
    parser.add_argument('--model_name', required=True,
                        help='Name of the model.')
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    test_data_dir = 'projects/' + args.model_name + '/test_data'
    print(test_data_dir)
    assert args.model_name in URLS, 'No sample test data available'
    url = URLS[args.model_name]

    if os.path.exists(test_data_dir):
        print('Test data exists at', test_data_dir)
        compressed_path = test_data_dir + '.tar.gz'
        # Extract the dataset.
        print('Extracting test data to', test_data_dir)
        with tarfile.open(compressed_path) as tar:
            tar.extractall(path=test_data_dir)
    else:
        os.makedirs(test_data_dir, exist_ok=True)
        # Download the compressed dataset.
        compressed_path = test_data_dir + '.tar.gz'
        if not os.path.exists(compressed_path):
            print('Downloading test data to', compressed_path)
            download_file_from_google_drive(url, compressed_path)

        # Extract the dataset.
        print('Extracting test data to', test_data_dir)
        with tarfile.open(compressed_path) as tar:
            tar.extractall(path=test_data_dir)


if __name__ == "__main__":
    main()
