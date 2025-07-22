import math

square = lambda x: x * x

factorial = lambda n: math.factorial(n)

reverse = lambda s: s[::-1]

uppercase = lambda s: s.upper()

filter_evens = lambda lst: list(filter(lambda x: x % 2 == 0, lst))

sum_of_list = lambda lst: sum(lst)

cube = lambda x: x ** 3

is_palindrome = lambda s: s == s[::-1]

multiply = lambda x, y: x * y

max_in_list = lambda lst: max(lst)

min_in_list = lambda lst: min(lst)

absolute_value = lambda x: abs(x)

power = lambda base, exp: base ** exp

length = lambda s: len(s)

capitalize_first = lambda s: s[0].upper() + s[1:] if s else ""

if __name__ == "__main__":
    print("Square of 5:", square(5))
    print("Factorial of 5:", factorial(5))
    print("Reverse of 'hello':", reverse("hello"))
    print("Uppercase of 'world':", uppercase("world"))
    print("Filter evens from [1,2,3,4,5,6]:", filter_evens([1,2,3,4,5,6]))
    print("Sum of [1,2,3,4,5]:", sum_of_list([1,2,3,4,5]))
    print("Cube of 3:", cube(3))
    print("Is 'radar' palindrome:", is_palindrome("radar"))
    print("Multiply 4 and 7:", multiply(4, 7))
    print("Max in [10,5,8,20,3]:", max_in_list([10,5,8,20,3]))
    print("Min in [10,5,8,20,3]:", min_in_list([10,5,8,20,3]))
    print("Absolute value of -15:", absolute_value(-15))
    print("2 to the power of 8:", power(2, 8))
    print("Length of 'python':", length("python"))
    print("Capitalize first letter of 'hello':", capitalize_first("hello"))
