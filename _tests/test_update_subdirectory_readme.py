import unittest
from unittest import mock


class MyTestCase(unittest.TestCase):
    @mock.patch('os.listdir')
    @mock.patch('os.path.isdir')
    @mock.patch('write_readme')
    def test_update_subdirectory_readme(self, mock_write_readme, mock_isdir, mock_listdir):
        mock_isdir.return_value = True
        mock_listdir.side_effect = lambda x: ['subdir1', 'subdir2'] if x == root_dir else ['file1.md', 'file2.md']

        update_subdirectory_readme(root_dir, ['subdir1', 'subdir2'])

        # Check if write_readme was called for each subdirectory
        self.assertEqual(mock_write_readme.call_count, 2)


if __name__ == '__main__':
  unittest.main()