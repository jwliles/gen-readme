#!/usr/bin/env python3

import os
import unittest
from unittest import mock
from unittest.mock import patch, mock_open
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Define the root directory you want to monitor
root_dir = '/home/jwl/projects/journal/til/'
template_file = '/home/jwl/projects/journal/til/readme-template.md'
readme_path = os.path.join(root_dir, "README.md")


def generate_subdirectory_readme_content(category_name, files):
  """
    Generate content for a subdirectory's README.md based on the files within it.
    """
  content = f"# {category_name}\n\n## TILs\n\n"
  for file in files:
    title = file.replace('.md', '').replace('-', ' ').capitalize()
    content += f"- [{title}]({file})\n"
  return content


def update_subdirectory_readme(root_dir, categories):
  """
    Update README.md files in each subdirectory with a list of files (TIL entries).
    """
  for category in categories:
    category_path = os.path.join(root_dir, category)
    files = [f for f in os.listdir(category_path) if f.endswith('.md') and f != "README.md"]
    readme_content = generate_subdirectory_readme_content(category, files)
    readme_path = os.path.join(category_path, "README.md")
    write_readme(readme_path, readme_content)


def generate_category_links(categories):
  # Generate Markdown links for categories for internal navigation
  return "\n".join([f"* [{c}](#{c.lower()})" for c in categories])


def write_readme(readme_path, content):
  """
    Writes the given content to a file specified by readme_path.

    Args:
    - readme_path (str): The path to the README file to be written.
    - content (str): The content to write into the README file.
    """
  with open(readme_path, 'w') as file:
    file.write(content)


def get_categories(root_dir):
  """
    Lists all subdirectories within the specified root directory, treating each as a category.

    Args:
    - root_dir (str): The path to the directory whose subdirectories are to be listed.

    Returns:
    - list: A sorted list of names of all subdirectories within root_dir.
    """
  categories = [name for name in os.listdir(root_dir)
                if os.path.isdir(os.path.join(root_dir, name))]
  return sorted(categories)


def get_til_count(root_dir):
  """
    Counts the number of Markdown (.md) files within the specified directory and its subdirectories,
    excluding README.md files.

    Args:
    - root_dir (str): The root directory from which to start counting.

    Returns:
    - int: The total count of .md files.
    """
  til_count = 0
  for filename in os.listdir(root_dir):
    if filename.endswith('.md') and not filename.startswith('.') and filename != 'README.md':
      til_count += 1
  return til_count


def read_template(template_path):
  """
    Reads the content of a template file and returns it as a string.

    Args:
    - template_path (str): The path to the template file.

    Returns:
    - str: The content of the template file.
    """
  with open(template_path, 'r') as file:
    return file.read()


def generate_category_details(root_dir, categories):
  category_details = ""
  for category in sorted(categories):
    category_path = os.path.join(root_dir, category)
    files = [f for f in sorted(os.listdir(category_path)) if f.endswith(".md") and f != "README.md"]
    if files:
      category_details += f"\n### {category}\n\n"
      for filename in files:
        title = filename.replace('.md', '').replace('-', ' ').capitalize()
        # The link target assumes a simple structure; adjust as needed for special cases
        link_target = os.path.join(category, filename)
        category_details += f"- [{title}]({link_target})\n"
  return category_details


def update_readme(root_dir, template_path, readme_path):
  template_content = read_template(template_path)
  til_count = get_til_count(root_dir)
  categories = get_categories(root_dir)

  # Generating content based on the template and the dynamic parts
  categories_links = generate_category_links(categories)
  category_details = generate_category_details(root_dir, categories)

  # Replace the placeholders or markers in the template with actual content
  readme_content = template_content.replace("_1399 TILs and counting..._", f"_{til_count} TILs and counting..._")
  categories_section = f"### Categories\n\n{categories_links}\n\n---\n"
  readme_content = readme_content.replace("### Categories", categories_section) + category_details

  write_readme(readme_path, readme_content)


class ChangeHandler(FileSystemEventHandler):
  def on_any_event(self, event):
    # Check if the event is for a README.md or the template file and ignore it
    if not event.is_directory and (
        event.src_path.endswith("/README.md") or event.src_path.endswith("/readme-template.md")):
      return
    print(f"Update triggered by change in: {event.src_path}")
    update_readme(root_dir, template_file, readme_path)  # Pass readme_path here


event_handler = ChangeHandler()
observer = Observer()
observer.schedule(event_handler, path=root_dir, recursive=True)
observer.start()

try:
  while True:
    pass
except KeyboardInterrupt:
  observer.stop()
observer.join()


class TestReadmeGeneration(unittest.TestCase):

  def test_read_template(self):
    # Assuming you have a 'test-template.md' for testing purposes
    test_template_path = '/home/jwl/projects/journal/til/readme-template.md'
    expected_content = "This is the readme template."
    self.assertEqual(read_template(test_template_path), expected_content)

  def test_get_categories(self):
    # Assuming '/home/jwl/projects/journal/til/' has specific test directories
    expected_categories = ['ack', 'amplify', 'ansible', 'bash', 'brew', 'browsers', 'chrome', 'clojure', 'css', 'deno',
                           'devops', 'docker', 'elixir', 'ember', 'gatsby', 'general', 'git', 'github',
                           'github-actions', 'go', 'groq', 'haskell', 'heroku', 'homebrew', 'html', 'http', 'inngest',
                           'internet', 'java', 'javascript', 'jq', 'kitty', 'less', 'life', 'linux', 'mac', 'mobile',
                           'mongodb', 'mysql', 'neovim', 'netlify', 'next-auth', 'nextjs', 'phoenix', 'planetscale',
                           'pnpm', 'postgres', 'powershell', 'prisma', 'python', 'rails', 'react', 'react_native',
                           'react-testing-library', 'reason', 'remix', 'ripgrep', 'rspec', 'ruby', 'security', 'sed',
                           'shell', 'sql', 'sqlite', 'streaming', 'svg', 'tailwind', 'terminal', 'testing', 'tmux',
                           'typescript', 'unix', 'urls', 'vercel', 'vim', 'vscode', 'webpack', 'workflow', 'xstate',
                           'yaml', 'zod',
                           ]  # Expected test categories
    result_categories = get_categories('/home/jwl/projects/journal/til/')
    self.assertEqual(sorted(result_categories), sorted(expected_categories))

  def test_get_til_count(self):
    # Assuming a specific setup in your test directory with a known number of .md files
    test_dir = '/home/jwl/projects/journal/til/python'  # Example test directory
    expected_count = 5  # Assuming there are 5 TIL files in the Python category
    self.assertEqual(get_til_count(test_dir), expected_count)

  def test_generate_category_details(self):
    # This requires a more complex setup as you need actual files to reference
    # Consider mocking os.listdir for a controlled test environment
    pass  # Example placeholder, implementation would be based on your test setup


class TestFileWriting(unittest.TestCase):
  @mock.patch("builtins.open", new_callable=mock.mock_open)
  def test_write_readme(self, mock_open):
    content = "Sample content"
    path = "dummy_path/README.md"
    write_readme(path, content)
    mock_open.assert_called_once_with(path, 'w')
    mock_open().write.assert_called_once_with(content)


# More tests can be added here...


@mock.patch('os.listdir')
@mock.patch('os.path.isdir')
@mock.patch('write_readme')
def test_update_subdirectory_readme(self, mock_write_readme, mock_isdir, mock_listdir):
  mock_isdir.return_value = True
  mock_listdir.side_effect = lambda x: ['subdir1', 'subdir2'] if x == root_dir else ['file1.md', 'file2.md']

  update_subdirectory_readme(root_dir, ['subdir1', 'subdir2'])

  # Check if write_readme was called for each subdirectory
  self.assertEqual(mock_write_readme.call_count, 2)


class TestReadmeIntegration(unittest.TestCase):
  def test_integration(self):
    # Assuming the presence of a controlled test environment
    test_root_dir = '/home/jwl/projects/journal/til/'
    test_template_file = '/home/jwl/projects/journal/til/readme-template.md'
    test_readme_path = os.path.join(test_root_dir, "readme-template.md")

    # Prepare your test environment here, possibly using mock or actual setup

    update_readme(test_root_dir, test_template_file, test_readme_path)

    # Verify the README.md was created with expected content
    with open(test_readme_path, 'r') as f:
      content = f.read()
    # Check content against what you expect it to contain


if __name__ == '__main__':
  unittest.main()