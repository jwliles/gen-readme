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