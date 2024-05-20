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