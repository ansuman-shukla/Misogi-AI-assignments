products = ["Laptop", "Mouse", "Keyboard", "Monitor"]
prices = [999.99, 25.50, 75.00, 299.99]
quantities = [5, 20, 15, 8]

product_price_pairs = list(zip(products, prices))
print("Product-Price Pairs:")
for product, price in product_price_pairs:
    print(f"{product}: ${price}")

print("\nTotal Value for Each Product:")
for product, price, quantity in zip(products, prices, quantities):
    total_value = price * quantity
    print(f"{product}: ${total_value:.2f}")

product_catalog = {}
for product, price, quantity in zip(products, prices, quantities):
    product_catalog[product] = {"price": price, "quantity": quantity}

print("\nProduct Catalog Dictionary:")
for product, details in product_catalog.items():
    print(f"{product}: {details}")

print("\nLow Stock Products:")
low_stock_products = [product for product, _, quantity in zip(products, prices, quantities) if quantity < 10]
for product in low_stock_products:
    print(product)
