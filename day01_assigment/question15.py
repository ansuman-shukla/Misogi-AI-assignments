library = []

def add_book():
    try:
        title = input("Enter book title: ").strip()
        author = input("Enter author name: ").strip()
        
        if not title or not author:
            print("Error: Title and author cannot be empty!")
            return
        
        book = {
            'title': title,
            'author': author
        }
        
        library.append(book)
        print(f"✓ Book '{title}' by {author} added successfully!")
        
    except Exception as e:
        print(f"Error adding book: {e}")

def search_book():
    if not library:
        print("Library is empty. Please add some books first.")
        return
    
    try:
        search_term = input("Enter book title or author to search: ").strip().lower()
        
        if not search_term:
            print("Search term cannot be empty!")
            return
        
        found_books = []
        for book in library:
            if (search_term in book['title'].lower() or 
                search_term in book['author'].lower()):
                found_books.append(book)
        
        if found_books:
            print(f"\n📚 Found {len(found_books)} book(s):")
            for i, book in enumerate(found_books, 1):
                print(f"{i}. Book: {book['title']} | Author: {book['author']}")
        else:
            print("No books found matching your search.")
            
    except Exception as e:
        print(f"Error searching book: {e}")

def display_inventory():
    if not library:
        print("📚 Library is empty. No books to display.")
        return
    
    try:
        print(f"\n📚 Library Inventory ({len(library)} books):")
        print("-" * 50)
        for i, book in enumerate(library, 1):
            print(f"{i}. Book: {book['title']} | Author: {book['author']}")
        print("-" * 50)
        
    except Exception as e:
        print(f"Error displaying inventory: {e}")

def display_menu():
    print("\n" + "="*40)
    print("📚 LIBRARY MANAGEMENT SYSTEM")
    print("="*40)
    print("1. Add Book")
    print("2. Search Book")
    print("3. Display Inventory")
    print("4. Exit")
    print("="*40)

def get_user_choice():
    try:
        choice = input("Enter your choice (1-4): ").strip()
        return choice
    except Exception as e:
        print(f"Error getting input: {e}")
        return None

def main():
    print("Welcome to the Library Management System!")
    
    while True:
        try:
            display_menu()
            choice = get_user_choice()
            
            if choice == '1':
                add_book()
            elif choice == '2':
                search_book()
            elif choice == '3':
                display_inventory()
            elif choice == '4':
                print("Thank you for using the Library Management System!")
                print("Goodbye! 👋")
                break
            else:
                print("❌ Invalid choice! Please enter a number between 1-4.")
                
        except KeyboardInterrupt:
            print("\n\nProgram interrupted by user. Goodbye! 👋")
            break
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
