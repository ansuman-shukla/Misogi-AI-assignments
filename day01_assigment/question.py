def celsius_to_fahrenheit(celsius):
    return (celsius * 9/5) + 32

def fahrenheit_to_kelvin(fahrenheit):
    return (fahrenheit - 32) * 5/9 + 273.15

def kelvin_to_celsius(kelvin):
    return kelvin - 273.15

def main():
    try:
        c_val = 0
        f_val = 32
        k_val = 300

        f_result = celsius_to_fahrenheit(c_val)
        k_result = fahrenheit_to_kelvin(f_val)
        c_result = kelvin_to_celsius(k_val)

        print(f"{c_val}°C = {f_result:.1f}°F")
        print(f"{f_val}°F = {k_result:.2f}K")
        print(f"{k_val}K = {c_result:.2f}°C")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
