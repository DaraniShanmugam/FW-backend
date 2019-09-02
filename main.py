import os
import json
import glob

def merge(input_files, output_dir, key, max_file_size=1024*1024, output_file_prefix='merged'):
    pass

def main():
    input_dir = 'data'
    input_file_prefix = 'input'

    output_dir = 'output'
    output_file_prefix = 'merged_'

    # Max file size of each output file in bytes
    max_file_size = 70

    key = 'strikers'

    input_path = os.path.join(
        input_dir, '{}*.json'.format(input_file_prefix))

    # List files sorted alphabetically
    input_files = glob.glob(input_path)

    if len(input_files) == 0:
        pass
        return

    # Sort based on counter value
    input_files.sort(key=lambda x: len(x))

    merge(input_files, output_dir, key, max_file_size, output_file_prefix)
    print('Done')


if __name__ == '__main__':
    main()
