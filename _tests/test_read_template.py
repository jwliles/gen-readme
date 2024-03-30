import unittest


class TestReadmeGeneration(unittest.TestCase):

  def test_read_template(self):
    # Assuming you have a 'test-template.md' for testing purposes
    test_template_path = '/home/jwl/projects/journal/til/readme-template.md'
    expected_content = "This is the readme template."
    self.assertEqual(read_template(test_template_path), expected_content)


if __name__ == '__main__':
  unittest.main()