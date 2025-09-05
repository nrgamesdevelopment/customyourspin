import os
import re

# Directory containing blog templates
blog_templates_dir = 'ads/templates/blog'

# Image mapping based on article categories
image_mapping = {
    'Fitness': "{% static 'images/blog/fitness-wheel.svg' %}",
    'Creators': "{% static 'images/blog/social-wheel.svg' %}",
    'Events': "{% static 'images/blog/event-wheel.svg' %}",
    'Education': "{% static 'images/blog/classroom-wheel.svg' %}",
    'Guide': "{% static 'images/blog/wheel-placeholder.svg' %}",
    'default': "{% static 'images/blog/wheel-placeholder.svg' %}"
}

# Pattern to match static image tags
static_image_pattern = r'<img src="{% static \'images/[^\']*\' %}"[^>]*>'

# Process each blog template
for filename in os.listdir(blog_templates_dir):
    if filename.endswith('.html') and filename != 'base.html' and filename != 'index.html':
        file_path = os.path.join(blog_templates_dir, filename)
        
        # Read the file content
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            content = file.read()
        
        # Check if the file contains static image tags
        if '{% static' in content and '<img src=' in content:
            # Find the tag category
            tag_match = re.search(r'<p class="tag">([^<]+)</p>', content)
            category = tag_match.group(1) if tag_match else 'default'
            
            # Get the appropriate image based on category
            new_image = image_mapping.get(category, image_mapping['default'])
            
            # Replace all image tags with the new image
            modified_content = re.sub(
                static_image_pattern, 
                f'<img src="{new_image}" alt="Custom wheel for {category}" class="blog-image">', 
                content
            )
            
            # Write the modified content back to the file
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(modified_content)
            
            print(f"Updated {filename} with {category} image")

print("All blog templates have been updated!")