import os
import json
import glob


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


def main():
    input_dir = 'input'
    input_file_prefix = 'data'

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
