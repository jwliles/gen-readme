#!/usr/bin/env python3

import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Define the root directory you want to monitor
root_dir = '/home/jwl/projects/journal/til/'
template_file = '/home/jwl/projects/journal/til/readme-template.md'
readme_path = os.path.join(root_dir, "README.md")


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