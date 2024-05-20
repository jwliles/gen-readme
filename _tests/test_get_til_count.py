import unittest


class MyTestCase(unittest.TestCase):
  def test_get_til_count(self):
    # Assuming a specific setup in your test directory with a known number of .md files
    test_dir = '/home/jwl/projects/journal/til/python'  # Example test directory
    expected_count = 5  # Assuming there are 5 TIL files in the Python category
    self.assertEqual(get_til_count(test_dir), expected_count)



if __name__ == '__main__':
  unittest.main()