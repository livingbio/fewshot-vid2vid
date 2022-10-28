import argparse
import os
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
            def is_within_directory(directory, target):
                
                abs_directory = os.path.abspath(directory)
                abs_target = os.path.abspath(target)
            
                prefix = os.path.commonprefix([abs_directory, abs_target])
                
                return prefix == abs_directory
            
            def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
            
                for member in tar.getmembers():
                    member_path = os.path.join(path, member.name)
                    if not is_within_directory(path, member_path):
                        raise Exception("Attempted Path Traversal in Tar File")
            
                tar.extractall(path, members, numeric_owner=numeric_owner) 
                
            
            safe_extract(tar, path=test_data_dir)
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
            def is_within_directory(directory, target):
                
                abs_directory = os.path.abspath(directory)
                abs_target = os.path.abspath(target)
            
                prefix = os.path.commonprefix([abs_directory, abs_target])
                
                return prefix == abs_directory
            
            def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
            
                for member in tar.getmembers():
                    member_path = os.path.join(path, member.name)
                    if not is_within_directory(path, member_path):
                        raise Exception("Attempted Path Traversal in Tar File")
            
                tar.extractall(path, members, numeric_owner=numeric_owner) 
                
            
            safe_extract(tar, path=test_data_dir)


if __name__ == "__main__":
    main()
