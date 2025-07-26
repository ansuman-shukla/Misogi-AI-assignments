fruits_list = ["apple", "banana", "orange", "apple", "grape"]
fruits_tuple = ("apple", "banana", "orange")
fruits_set = {"apple", "banana", "orange", "grape"}
fruits_dict = {"apple": 5, "banana": 3, "orange": 8, "grape": 2}

print("1. Check for Membership")
print(f"'apple' in fruits_list: {'apple' in fruits_list}")
print(f"'apple' in fruits_tuple: {'apple' in fruits_tuple}")
print(f"'apple' in fruits_set: {'apple' in fruits_set}")
print(f"'apple' in fruits_dict: {'apple' in fruits_dict}")

print("\n2. Find Length")
print(f"Length of fruits_list: {len(fruits_list)}")
print(f"Length of fruits_tuple: {len(fruits_tuple)}")
print(f"Length of fruits_set: {len(fruits_set)}")
print(f"Length of fruits_dict: {len(fruits_dict)}")

print("\n3. Iterate and Print Elements")
print("fruits_list contents:")
for fruit in fruits_list:
    print(fruit)

print("\nfruits_tuple contents:")
for fruit in fruits_tuple:
    print(fruit)

print("\nfruits_set contents:")
for fruit in fruits_set:
    print(fruit)

print("\nfruits_dict contents:")
for key in fruits_dict:
    print(key)

print("\n4. Compare Membership Testing Performance")
print("Sets are most efficient for membership testing due to hash-based lookup (O(1) average case)")
print("Lists and tuples require linear search (O(n) worst case)")
print("Dictionaries are efficient for key membership testing (O(1) average case)")

print("\n5. Demonstrate Different Iteration Patterns")
print("Iterating fruits_set with for item in set:")
for item in fruits_set:
    print(item)

print("\nIterating fruits_dict with for key in dict:")
for key in fruits_dict:
    print(f"Key: {key}")

print("\nIterating fruits_dict with for key, value in dict.items():")
for key, value in fruits_dict.items():
    print(f"Key: {key}, Value: {value}")
