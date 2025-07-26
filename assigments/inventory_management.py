inventory = {
    "apples": {"price": 1.50, "quantity": 100},
    "bananas": {"price": 0.75, "quantity": 150},
    "oranges": {"price": 2.00, "quantity": 80}
}

def add_product(name, price, quantity):
    inventory[name] = {"price": price, "quantity": quantity}

def update_price(product_name, new_price):
    if product_name in inventory:
        inventory[product_name]["price"] = new_price

def sell_product(product_name, quantity_sold):
    if product_name in inventory and inventory[product_name]["quantity"] >= quantity_sold:
        inventory[product_name]["quantity"] -= quantity_sold

def calculate_total_value():
    total = 0
    for product in inventory:
        total += inventory[product]["price"] * inventory[product]["quantity"]
    return total

def find_low_stock_products(threshold=100):
    low_stock = []
    for product in inventory:
        if inventory[product]["quantity"] < threshold:
            low_stock.append(product)
    return low_stock

add_product("grapes", 3.25, 60)
update_price("bananas", 0.80)
sell_product("apples", 25)

print("Current Inventory:")
for product, details in inventory.items():
    print(f"{product}: Price=${details['price']:.2f}, Quantity={details['quantity']}")

print(f"\nTotal Inventory Value: ${calculate_total_value():.2f}")

low_stock = find_low_stock_products()
if low_stock:
    print(f"\nLow Stock Products: {', '.join(low_stock)}")
else:
    print("\nNo low stock products")
