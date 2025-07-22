try:
    name = input("Enter your full name: ")
    age = input("Enter your age: ")
    city = input("Enter your city: ")
    hobby = input("Enter your hobby: ")

    print(f"\nHello, {name}!")
    print(f"You are {age} years old and live in {city}.")
    print(f"In your free time, you enjoy {hobby}.")

except Exception as e:
    print(f"An error occurred: {e}")
