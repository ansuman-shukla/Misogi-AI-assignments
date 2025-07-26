from collections import Counter
import re
import string

def analyze_text(text):
    if not text:
        return {}
    
    text_lower = text.lower()
    
    chars = list(text)
    char_count = len(chars)
    
    words = re.findall(r'\b\w+\b', text_lower)
    word_count = len(words)
    
    sentences = re.split(r'[.!?]+', text.strip())
    sentences = [s for s in sentences if s.strip()]
    sentence_count = len(sentences)
    
    paragraphs = [p for p in text.split('\n\n') if p.strip()]
    paragraph_count = len(paragraphs)
    
    vowels = 'aeiou'
    vowel_count = sum(1 for char in text_lower if char in vowels)
    consonant_count = sum(1 for char in text_lower if char.isalpha() and char not in vowels)
    
    char_frequency = Counter(text_lower)
    word_frequency = Counter(words)
    
    most_common_char = char_frequency.most_common(1)[0] if char_frequency else ('', 0)
    most_common_word = word_frequency.most_common(1)[0] if word_frequency else ('', 0)
    
    unique_words = len(set(words))
    unique_chars = len(set(text_lower))
    
    punctuation_count = sum(1 for char in text if char in string.punctuation)
    digit_count = sum(1 for char in text if char.isdigit())
    uppercase_count = sum(1 for char in text if char.isupper())
    lowercase_count = sum(1 for char in text if char.islower())
    whitespace_count = sum(1 for char in text if char.isspace())
    
    avg_word_length = sum(len(word) for word in words) / len(words) if words else 0
    avg_sentence_length = word_count / sentence_count if sentence_count > 0 else 0
    
    return {
        'total_characters': char_count,
        'total_words': word_count,
        'total_sentences': sentence_count,
        'total_paragraphs': paragraph_count,
        'vowel_count': vowel_count,
        'consonant_count': consonant_count,
        'unique_words': unique_words,
        'unique_characters': unique_chars,
        'punctuation_count': punctuation_count,
        'digit_count': digit_count,
        'uppercase_count': uppercase_count,
        'lowercase_count': lowercase_count,
        'whitespace_count': whitespace_count,
        'average_word_length': round(avg_word_length, 2),
        'average_sentence_length': round(avg_sentence_length, 2),
        'most_common_character': most_common_char,
        'most_common_word': most_common_word,
        'character_frequency': dict(char_frequency.most_common(10)),
        'word_frequency': dict(word_frequency.most_common(10))
    }

def get_word_frequency_with_length(text, length=None):
    words = re.findall(r'\b\w+\b', text.lower())
    if length:
        words = [word for word in words if len(word) == length]
    return Counter(words)

def find_common_words_between_texts(text1, text2):
    words1 = set(re.findall(r'\b\w+\b', text1.lower()))
    words2 = set(re.findall(r'\b\w+\b', text2.lower()))
    return words1.intersection(words2)

def compare_with_statistics(text, other_text):
    stats1 = analyze_text(text)
    stats2 = analyze_text(other_text)
    
    common_words = find_common_words_between_texts(text, other_text)
    
    similarity_score = len(common_words) / max(stats1['unique_words'], stats2['unique_words']) if max(stats1['unique_words'], stats2['unique_words']) > 0 else 0
    
    return {
        'text1_stats': stats1,
        'text2_stats': stats2,
        'common_words': list(common_words),
        'common_word_count': len(common_words),
        'similarity_score': round(similarity_score, 3)
    }

def main():
    sample_text = """
    This is a sample text for analysis. It contains multiple sentences and paragraphs.
    The text has various characters, numbers like 123, and punctuation marks!
    
    This is the second paragraph. It demonstrates how the text analysis tool works.
    The tool can count words, characters, sentences, and much more.
    """
    
    analysis = analyze_text(sample_text)
    
    print("Text Analysis Results:")
    print("=" * 50)
    for key, value in analysis.items():
        if isinstance(value, dict):
            print(f"{key.replace('_', ' ').title()}:")
            for k, v in value.items():
                print(f"  {k}: {v}")
        else:
            print(f"{key.replace('_', ' ').title()}: {value}")
    
    print("\n" + "=" * 50)
    print("Word frequency by length (3 characters):")
    length_freq = get_word_frequency_with_length(sample_text, 3)
    for word, count in length_freq.most_common(5):
        print(f"{word}: {count}")
    
    other_text = "This is another sample text. It has some common words with the first text."
    comparison = compare_with_statistics(sample_text, other_text)
    
    print(f"\nCommon words between texts: {comparison['common_words']}")
    print(f"Similarity score: {comparison['similarity_score']}")

if __name__ == "__main__":
    main()
