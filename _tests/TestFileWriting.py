class TestFileWriting(unittest.TestCase):
    @mock.patch("builtins.open", new_callable=mock.mock_open)
    def test_write_readme(self, mock_open):
        content = "Sample content"
        path = "dummy_path/README.md"
        write_readme(path, content)
        mock_open.assert_called_once_with(path, 'w')
        mock_open().write.assert_called_once_with(content)


import unittest


class MyTestCase(unittest.TestCase):
  def test_something(self):
    self.assertEqual(True, False)  # add assertion here


if __name__ == '__main__':
  unittest.main()