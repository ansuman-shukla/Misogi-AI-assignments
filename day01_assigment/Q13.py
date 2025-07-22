try:
    price1 = float(input("Enter price of item 1: "))
    quantity1 = int(input("Enter quantity of item 1: "))

    price2 = float(input("Enter price of item 2: "))
    quantity2 = int(input("Enter quantity of item 2: "))

    price3 = float(input("Enter price of item 3: "))
    quantity3 = int(input("Enter quantity of item 3: "))

    total1 = price1 * quantity1
    total2 = price2 * quantity2
    total3 = price3 * quantity3

    subtotal = total1 + total2 + total3
    tax_rate = 0.085
    tax_amount = subtotal * tax_rate
    final_total = subtotal + tax_amount

    print("\n--- RECEIPT ---")
    print(f"Item 1: {quantity1} x ${price1:.2f} = ${total1:.2f}")
    print(f"Item 2: {quantity2} x ${price2:.2f} = ${total2:.2f}")
    print(f"Item 3: {quantity3} x ${price3:.2f} = ${total3:.2f}")
    print("-----------------")
    print(f"Subtotal: ${subtotal:.2f}")
    print(f"Tax (8.5%): ${tax_amount:.2f}")
    print(f"Total: ${final_total:.2f}")
    print("-----------------")

except ValueError:
    print("Invalid input. Please enter numbers only.")
except Exception as e:
    print(f"An error occurred: {e}")
