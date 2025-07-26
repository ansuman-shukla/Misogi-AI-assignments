def add_item(cart, item):
    cart.append(item)

def remove_specific_item(cart, item):
    if item in cart:
        cart.remove(item)

def remove_last_item(cart):
    if cart:
        cart.pop()

def display_alphabetical(cart):
    sorted_cart = sorted(cart)
    for item in sorted_cart:
        print(item)

def display_with_indices(cart):
    for i, item in enumerate(cart):
        print(f"{i}: {item}")

def shopping_cart_demo():
    cart = []
    
    add_item(cart, "apples")
    add_item(cart, "bread")
    add_item(cart, "milk")
    add_item(cart, "eggs")
    
    remove_specific_item(cart, "bread")
    
    remove_last_item(cart)
    
    display_alphabetical(cart)
    
    display_with_indices(cart)

if __name__ == "__main__":
    shopping_cart_demo()
