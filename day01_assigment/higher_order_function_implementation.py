def custom_map(func, iterable):
    return [func(x) for x in iterable]

def custom_filter(func, iterable):
    return [x for x in iterable if func(x)]

def custom_reduce(func, iterable):
    result = iterable[0]
    for x in iterable[1:]:
        result = func(result, x)
    return result

if __name__ == "__main__":
    print(custom_map(lambda x: x * 2, [1, 2, 3]))
    print(custom_filter(lambda x: x % 2 == 0, [1, 2, 3, 4]))
    print(custom_reduce(lambda x, y: x + y, [1, 2, 3, 4]))
