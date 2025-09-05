import os
import re

# Directory containing blog templates
blog_templates_dir = 'ads/templates/blog'

# Pattern to match static image tags
static_image_pattern = r'<img src="{% static \'images/[^\']*\' %}"'

# Replacement with new image paths
replacement_svg = '<img src="{% static \'images/blog-image.svg\' %}"'
replacement_png = '<img src="{% static \'images/blog-image.png\' %}"'

# Process each blog template
for filename in os.listdir(blog_templates_dir):
    if filename.endswith('.html') and filename != 'base.html' and filename != 'index.html':
        file_path = os.path.join(blog_templates_dir, filename)
        
        # Read the file content
        with open(file_path, 'r') as file:
            content = file.read()
        
        # Check if the file contains static image tags
        if '{% static' in content and '<img src=' in content:
            # Replace the first occurrence with SVG
            modified_content = re.sub(static_image_pattern, replacement_svg, content, count=1)
            
            # Replace any additional occurrences with PNG
            modified_content = re.sub(static_image_pattern, replacement_png, modified_content)
            
            # Write the modified content back to the file
            with open(file_path, 'w') as file:
                file.write(modified_content)
            
            print(f"Updated {filename}")

print("All blog templates have been updated!")