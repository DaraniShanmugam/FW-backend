import unittest
from main import merge
import glob
import os
from tempfile import TemporaryDirectory

class Test(unittest.TestCase):

    def testFileContentsEqual(self):
        input_path = os.path.join(
            'input', '{}*.json'.format('data'))
        input_files = glob.glob(input_path)
        if len(input_files) == 0:
            print('No JSON files found.')
            print('Check if you have entered the path correctly.')
            print()
            return
        # Sort based on counter value
        input_files.sort(key=lambda x: len(x))

        merge(input_files, 'output', 'strikers', 70, 'merged')

        #Tests the number of files in output
        output_dir = os.path.join('output')
        test_dir = os.path.join('testoutput')
        no_of_files = (len([name for name in os.listdir(output_dir) if os.path.isfile(os.path.join(output_dir, name))]))
        self.assertEqual(no_of_files, 4)

        #Tests each file size is equal in temproray and output folder
        content1 = []
        content2 = []
        for i in os.listdir(output_dir):
            content1.append(os.path.getsize(os.path.join(output_dir,i)))
        for i in os.listdir(test_dir):
            content2.append(os.path.getsize(os.path.join(test_dir, i)))
        for i in range(len(content1)):
            self.assertEqual(content1[i], content2[i])


if __name__ == '__main__':
    unittest.main()