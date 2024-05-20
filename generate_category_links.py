def generate_category_links(categories):
    # Generate Markdown links for categories for internal navigation
    return "\n".join([f"* [{c}](#{c.lower()})" for c in categories])