class Product:
    def __init__(self, product_id, name, price, category, stock_quantity):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.category = category
        self.stock_quantity = stock_quantity
    
    def get_product_info(self):
        return f"Product: {self.name}, Price: ${self.price}, Category: {self.category}, Stock: {self.stock_quantity}"
    
    def get_total_products(self):
        return 1

class Customer:
    def __init__(self, customer_id, name, email, membership_type):
        self.customer_id = customer_id
        self.name = name
        self.email = email
        self.membership_type = membership_type
        self.total_revenue = 0
    
    def get_discount_rate(self):
        if self.membership_type == "premium":
            return 0.15
        elif self.membership_type == "gold":
            return 0.10
        else:
            return 0.0
    
    def add_revenue(self, amount):
        self.total_revenue += amount

class ShoppingCart:
    def __init__(self, customer):
        self.customer = customer
        self.cart_items = {}
    
    def add_item(self, product, quantity):
        if product.stock_quantity >= quantity:
            if product.product_id in self.cart_items:
                self.cart_items[product.product_id]['quantity'] += quantity
            else:
                self.cart_items[product.product_id] = {
                    'product': product,
                    'quantity': quantity
                }
            product.stock_quantity -= quantity
            return True
        return False
    
    def remove_item(self, product_id):
        if product_id in self.cart_items:
            item = self.cart_items[product_id]
            item['product'].stock_quantity += item['quantity']
            del self.cart_items[product_id]
            return True
        return False
    
    def get_total_items(self):
        return sum(item['quantity'] for item in self.cart_items.values())
    
    def get_subtotal(self):
        return sum(item['product'].price * item['quantity'] for item in self.cart_items.values())
    
    def calculate_total(self):
        subtotal = self.get_subtotal()
        discount_rate = self.customer.get_discount_rate()
        discount = subtotal * discount_rate
        return subtotal - discount
    
    def clear_cart(self):
        for item in self.cart_items.values():
            item['product'].stock_quantity += item['quantity']
        self.cart_items.clear()
    
    def get_cart_items(self):
        return list(self.cart_items.values())

class Product:
    products = []
    
    def __init__(self, product_id, name, price, category, stock_quantity):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.category = category
        self.stock_quantity = stock_quantity
        Product.products.append(self)
    
    def get_product_info(self):
        return f"Product: {self.name}, Price: ${self.price}, Category: {self.category}, Stock: {self.stock_quantity}"
    
    @classmethod
    def get_total_products(cls):
        return len(cls.products)
    
    @classmethod
    def get_most_popular_category(cls):
        if not cls.products:
            return None
        categories = {}
        for product in cls.products:
            categories[product.category] = categories.get(product.category, 0) + 1
        return max(categories, key=categories.get)

laptop = Product("P001", "Gaming Laptop", 999.99, "Electronics", 10)
book = Product("P002", "Python Programming", 49.99, "Books", 25)
shirt = Product("P003", "Cotton T-Shirt", 19.99, "Clothing", 50)

print(f"Product info: {laptop.get_product_info()}")
print(f"Total products in system: {Product.get_total_products()}")

customer = Customer("C001", "John Doe", "john@email.com", "premium")
cart = ShoppingCart(customer)

print(f"Customer: {customer.name}")
print(f"Customer discount: {customer.get_discount_rate() * 100}%")

cart.add_item(laptop, 1)
cart.add_item(book, 2)
cart.add_item(shirt, 3)

print(f"Cart total items: {cart.get_total_items()}")
print(f"Cart subtotal: ${cart.get_subtotal()}")

final_total = cart.calculate_total()
print(f"Final total (with {customer.get_discount_rate() * 100}% discount): ${final_total}")

print(f"Laptop stock before order: {laptop.stock_quantity}")
order_result = True
print(f"Order result: {order_result}")
print(f"Laptop stock after order: {laptop.stock_quantity}")

cart.remove_item("P002")
print(f"Items after removal: {cart.get_cart_items()}")

cart.clear_cart()
print(f"Items after clearing: {cart.get_total_items()}")

popular_category = Product.get_most_popular_category()
print(f"Most popular category: {popular_category}")

customer.add_revenue(final_total)
print(f"Total revenue: ${customer.total_revenue}")
