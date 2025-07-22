try:
    user_input = input("Enter Your age: ")
    if not user_input.isdigit():
        raise ValueError("Invalid input: Please enter a valid age.")
    user_input = int(user_input)
    if user_input <= 0:
        raise ValueError("Invalid input: Age must be a positive integer.")
except ValueError as e:
    print(e)