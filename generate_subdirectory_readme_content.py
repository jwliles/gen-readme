def generate_subdirectory_readme_content(category_name, files):
  """
    Generate content for a subdirectory's README.md based on the files within it.
    """
  content = f"# {category_name}\n\n## TILs\n\n"
  for file in files:
    title = file.replace('.md', '').replace('-', ' ').capitalize()
    content += f"- [{title}]({file})\n"
  return content