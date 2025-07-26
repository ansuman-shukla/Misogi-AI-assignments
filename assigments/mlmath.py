def dot_product(a, b):
    if len(a) != len(b):
        raise ValueError("Vectors must have the same length")
    return sum(x * y for x, y in zip(a, b))


def matrix_multiply(A, B):
    if len(A[0]) != len(B):
        raise ValueError("Number of columns in A must equal number of rows in B")
    
    result = []
    for i in range(len(A)):
        row = []
        for j in range(len(B[0])):
            element = sum(A[i][k] * B[k][j] for k in range(len(B)))
            row.append(element)
        result.append(row)
    return result


def conditional_probability(events):
    if not events:
        return 0.0
    
    total_events = len(events)
    favorable_events = sum(1 for event in events if event)
    
    return favorable_events / total_events


if __name__ == "__main__":
    print("mlmath library - Example usage:")
    
    vec1 = [1, 2, 3]
    vec2 = [4, 5, 6]
    print(f"Dot product of {vec1} and {vec2}: {dot_product(vec1, vec2)}")
    
    matrix_a = [[1, 2], [3, 4]]
    matrix_b = [[5, 6], [7, 8]]
    print(f"Matrix multiplication result: {matrix_multiply(matrix_a, matrix_b)}")
    
    events_list = [True, False, True, True, False]
    print(f"Conditional probability: {conditional_probability(events_list)}")
