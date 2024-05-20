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