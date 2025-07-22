from functools import reduce

squares_even = [i*i for i in range(1, 11) if i % 2 == 0]

capitalized_words = list(map(str.capitalize, ['hello', 'world']))

sum_numbers = reduce(lambda x, y: x + y, [1, 2, 3, 4])

filtered_positive = list(filter(lambda x: x > 0, [-2, -1, 0, 1, 2]))

word_lengths = {word: len(word) for word in ['apple', 'banana', 'cherry']}
