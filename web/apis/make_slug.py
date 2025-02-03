import random
import string

def generate_random_id(k=8):
    """Generate a random alphanumeric ID."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=k)).lower()

def make_slug(text):
    """Generate a slug from the given text with a random ID."""
    # Generate a random ID
    id = generate_random_id()

    # Extract the first 20 characters of the text
    text_prefix = text[:30]
    
    # Remove any non-alphanumeric characters and replace spaces with hyphens
    cleaned_text = ''.join(c if c.isalnum() else '-' for c in text_prefix.strip()).strip('-')
    
    # Combine the cleaned text and the ID to create the slug
    slug = f"{cleaned_text}-{id}"
    
    return slug.lower()

""" # Example usage:
text = "This is a long text with some characters."
slug = make_slug(text)
print(slug)  # Output example: 'This-is-a-long-text-q7ZwF9Xv'
 """