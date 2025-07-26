def add_vectors(a, b):
    return [a[i] + b[i] for i in range(len(a))]

def dot_product(a, b):
    return sum(a[i] * b[i] for i in range(len(a)))

def are_orthogonal(a, b):
    return dot_product(a, b) == 0

def multiply_matrices(A, B):
    rows_A = len(A)
    cols_A = len(A[0])
    cols_B = len(B[0])
    
    result = [[0 for _ in range(cols_B)] for _ in range(rows_A)]
    
    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                result[i][j] += A[i][k] * B[k][j]
    
    return result

if __name__ == "__main__":
    a = [1, 2, 3]
    b = [4, 5, 6]
    
    print("Sum:", add_vectors(a, b))
    print("Dot Product:", dot_product(a, b))
    print("Orthogonal:", are_orthogonal(a, b))
    
    A = [[1, 2], [3, 4]]
    B = [[5, 6], [7, 8]]
    
    print("Matrix Multiplication:", multiply_matrices(A, B))
