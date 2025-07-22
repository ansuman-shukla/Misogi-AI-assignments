def create_squares_traditional():
    squares = []
    for i in range(10):
        squares.append(i * i)
    return squares

def create_squares_comprehension():
    return [i * i for i in range(10)]

def create_evens_filtered():
    return [i for i in range(10) if i % 2 == 0]

def create_nested_pairs():
    return [(x, y) for x in range(3) for y in range(2)]

def convert_to_comprehension(numbers):
    return [x * x for x in numbers]

def filter_even_squares(numbers):
    return [x * x for x in numbers if x % 2 == 0]

def create_multiplication_table(n):
    return [[i * j for j in range(1, n + 1)] for i in range(1, n + 1)]

def flatten_nested_list(nested_list):
    return [item for sublist in nested_list for item in sublist]

def create_dict_comprehension(keys, values):
    return {k: v for k, v in zip(keys, values)}

def filter_strings_by_length(strings, min_length):
    return [s for s in strings if len(s) >= min_length]

def create_set_comprehension(numbers):
    return {x * x for x in numbers}

def conditional_transformation(numbers):
    return [x * 2 if x % 2 == 0 else x * 3 for x in numbers]

def main():
    print("Traditional for loop:")
    traditional_squares = create_squares_traditional()
    print(traditional_squares)
    
    print("\nList comprehension:")
    comprehension_squares = create_squares_comprehension()
    print(comprehension_squares)
    
    print("\nFiltered evens:")
    evens = create_evens_filtered()
    print(evens)
    
    print("\nNested loops (pairs):")
    pairs = create_nested_pairs()
    print(pairs)
    
    sample_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    
    print("\nSquares of sample numbers:")
    squares = convert_to_comprehension(sample_numbers)
    print(squares)
    
    print("\nSquares of even numbers only:")
    even_squares = filter_even_squares(sample_numbers)
    print(even_squares)
    
    print("\nMultiplication table (5x5):")
    mult_table = create_multiplication_table(5)
    for row in mult_table:
        print(row)
    
    print("\nFlattened nested list:")
    nested = [[1, 2], [3, 4], [5, 6]]
    flattened = flatten_nested_list(nested)
    print(flattened)
    
    print("\nDictionary comprehension:")
    keys = ['a', 'b', 'c']
    values = [1, 2, 3]
    dict_comp = create_dict_comprehension(keys, values)
    print(dict_comp)
    
    print("\nFiltered strings by length:")
    strings = ['python', 'java', 'c', 'javascript', 'go']
    long_strings = filter_strings_by_length(strings, 4)
    print(long_strings)
    
    print("\nSet comprehension (unique squares):")
    numbers_with_duplicates = [1, 2, 2, 3, 3, 4, 5]
    unique_squares = create_set_comprehension(numbers_with_duplicates)
    print(unique_squares)
    
    print("\nConditional transformation:")
    transformed = conditional_transformation(sample_numbers)
    print(transformed)

if __name__ == "__main__":
    main()
