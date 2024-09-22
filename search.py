# Initialize the catalog as an empty dictionary
catalog = {}

# Function to add a new category
def add_category(category_name):
    if category_name not in catalog:
        catalog[category_name] = []
        print(f"Category '{category_name}' added successfully.")
    else:
        print(f"Category '{category_name}' already exists.")

# Function to add a product to an existing category
def add_product(category_name, product_name):
    if category_name in catalog:
        catalog[category_name].append(product_name)
        print(f"Product '{product_name}' added to category '{category_name}'.")
    else:
        print(f"Category '{category_name}' does not exist. Please add the category first.")

# Function to display all categories and products
def display_catalog():
    if catalog:
        print("Product Catalog:")
        for category, products in catalog.items():
            print(f"Category: {category}")
            if products:
                for product in products:
                    print(f"  - {product}")
            else:
                print("  No products in this category.")
    else:
        print("The catalog is empty.")

# Function to search for a product across all categories
def search_product(product_name):
    found = False
    for category, products in catalog.items():
        if product_name in products:
            print(f"Product '{product_name}' found in category '{category}'.")
            found = True
    if not found:
        print(f"Product '{product_name}' not found in the catalog.")

# Error handling for adding multiple products and searches
def handle_additions():
    while True:
        option = input("Enter '1' to add category, '2' to add product, '3' to display catalog, '4' to search product, or 'q' to quit: ")
        if option == '1':
            category = input("Enter the category name: ")
            add_category(category)
        elif option == '2':
            category = input("Enter the category name: ")
            product = input("Enter the product name: ")
            add_product(category, product)
        elif option == '3':
            display_catalog()
        elif option == '4':
            product = input("Enter the product name to search: ")
            search_product(product)
        elif option == 'q':
            print("Exiting...")
            break
        else:
            print("Invalid option, please try again.")

# Start the program
handle_additions()
