# String tools for various string operations

def reverse_string(s):
    """Reverse a string"""
    return s[::-1]

def count_characters(s):
    """Count the number of characters in a string"""
    return len(s)

def count_words(s):
    """Count the number of words in a string"""
    return len(s.split())

def to_uppercase(s):
    """Convert string to uppercase"""
    return s.upper()

def to_lowercase(s):
    """Convert string to lowercase"""
    return s.lower()

def capitalize_words(s):
    """Capitalize the first letter of each word"""
    return s.title()

def remove_whitespace(s):
    """Remove leading and trailing whitespace"""
    return s.strip()

def replace_substring(s, old, new):
    """Replace occurrences of old substring with new substring"""
    return s.replace(old, new)

def is_palindrome(s):
    """Check if a string is a palindrome"""
    cleaned = s.lower().replace(' ', '')
    return cleaned == cleaned[::-1]
