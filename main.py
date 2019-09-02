import os
import json
import glob
import sys
import argparse

def merge(input_files, output_dir, key, max_file_size=1024*1024, output_file_prefix='merged'):
    # Ensure if input exists
    if len(input_files) == 0:
        return

    # Ensure if output dir exists or create new
    os.makedirs(output_dir, exist_ok=True)

    # Get base size of JSON object excluding data
    # eg: {"strikers": []}
    base_prefix = '{{"{}": ['.format(key).encode()
    base_suffix = ']}'.encode()
    base_size = len(base_prefix+base_suffix)

    out_count_suffix = 1

    out_data = base_prefix
    out_size = base_size

    for in_file in input_files:
        try:
            data = json.load(open(in_file))
        except json.JSONDecodeError as e:
            print('Invalid JSON file {}. Skipping.'.format(in_file))
            print()
            continue

        if key not in data:
            print('Key {} not in {}. Skipping file'.format(key, in_file))
            print()
            continue

        data = data[key]

        cur_index = 0
        while cur_index < len(data):
            item = data[cur_index]
            item = json.dumps(item).encode()

            # Add comma and space if not the first item
            if out_data != base_prefix:
                item = ', '.encode() + item

            item_size = len(item)

            if item_size + base_size > max_file_size:
                # Item too large. Cannot be stored in any file as
                # it exceeds MAX_LENGTH. Skip the record.
                print('Record larger than max length. Skipping.')
                print('File: {}, Index: {}'.format(in_file, cur_index))
                print()
                cur_index += 1

            elif (out_size + item_size) > max_file_size:
                # Current file size cannot hold this record.
                # Save current and move to next file.
                out_data += base_suffix

                cur_file = '{}{}.json'.format(
                    output_file_prefix, out_count_suffix)

                with open(os.path.join(output_dir, cur_file), 'wb') as fp:
                    fp.write(out_data)

                out_count_suffix += 1
                out_data = base_prefix
                out_size = base_size

            else:
                out_data += item
                out_size += item_size
                cur_index += 1

    cur_file = '{}{}.json'.format(output_file_prefix, out_count_suffix)
    out_data += base_suffix
    with open(os.path.join(output_dir, cur_file), 'wb') as fp:
        fp.write(out_data)

def create_arg_parser():
    """"Creates and returns the ArgumentParser object."""

    parser = argparse.ArgumentParser()
    parser.add_argument('inputdir')
    parser.add_argument('outputdir')
    parser.add_argument('key')
    parser.add_argument('-i', "--inprefix", dest='iprefix',
                        help='Prefix for JSON files under inputdir [Default: input]', default='input')
    parser.add_argument('-o', "--outprefix", dest='oprefix',
                        help='Prefix for JSON files to store under outputdir [Default: merged]', default='merged')
    parser.add_argument('-m', "--max", dest='max',
                        help='Maximum file size for output in bytes. [Default: 1MB]', default=1024*1024, type=int)
    return parser


def main():
    arg_parser = create_arg_parser().parse_args()

    input_dir = arg_parser.inputdir
    input_file_prefix = arg_parser.iprefix

    output_dir = arg_parser.outputdir
    output_file_prefix = arg_parser.oprefix

    # Max file size of each output file in bytes
    max_file_size = arg_parser.max
    key = arg_parser.key
    input_path = os.path.join(
        input_dir, '{}*.json'.format(input_file_prefix))

    # List files sorted alphabetically
    input_files = glob.glob(input_path)

    if len(input_files) == 0:
        print('No JSON files found.')
        print('Check if you have entered the path correctly.')
        print()
        return

    # Sort based on counter value
    input_files.sort(key=lambda x: len(x))

    merge(input_files, output_dir, key, max_file_size, output_file_prefix)
    print('Done')


if __name__ == '__main__':
    main()
