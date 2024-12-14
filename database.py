import mysql.connector

# Database connection setup
def connect_db():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",  
        password="",  
        database="recipe_app"  # name of the database 
    )
    return conn

# Create tables if they don't exist
def create_tables():
    conn = connect_db()
    cursor = conn.cursor()

    # Create 'users' table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL
        );
    """)

    # Create 'recipes' table with a foreign key reference to 'users' table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS recipes (
            recipe_id INT AUTO_INCREMENT PRIMARY KEY,
            food_name VARCHAR(255) NOT NULL UNIQUE,
            ingredients TEXT NOT NULL,
            meal_type VARCHAR(255) NOT NULL,
            user_id INT,  -- Foreign Key to 'users' table
            FOREIGN KEY (user_id) REFERENCES users(user_id)  
        );
    """)

    conn.commit()
    conn.close()

# User Registration
def register(username, password):
    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        conn.commit()
        print(f"Registration successful for {username}!\n")
        conn.close()
        return True  # Registration success
    except mysql.connector.errors.IntegrityError:
        print(f"Username {username} already exists. Try another.\n")
        conn.close()
        return False  # Registration failed due to username conflict

# User Login
def login(username, password):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT user_id, password FROM users WHERE username = %s", (username,))
    result = cursor.fetchone()

    conn.close()

    if result and result[1] == password:
        print(f"Login successful for {username}!\n")
        return result[0]  # Return user ID
    else:
        print("Invalid username or password.\n")
        return None  # Invalid login

# Search for a Recipe (including ingredients)
def search_recipe(food_name):
    print("\n=== Search Food Recipe ===")

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT ingredients, meal_type FROM recipes WHERE food_name = %s", (food_name,))
    result = cursor.fetchone()

    if result:
        ingredients, meal_type = result
        print(f"Recipe for {food_name}:\nIngredients:\n{ingredients}\nMeal Type: {meal_type}")
    else:
        print(f"No recipe found for {food_name}.")

    conn.close()

# Add a Recipe (including ingredients and meal_type)
def add_recipe(user_id, food_name, ingredients, meal_type):
    print("\n=== Add Food Recipe ===")

    conn = connect_db()
    cursor = conn.cursor()

    # Check if the food already exists
    cursor.execute("SELECT * FROM recipes WHERE food_name = %s", (food_name,))
    if cursor.fetchone():
        print(f"{food_name} already exists. Use 'Update Food Recipe' to modify it.")
        conn.close()
        return False  # Recipe already exists

    # Insert the recipe with the foreign key (user_id)
    cursor.execute("INSERT INTO recipes (food_name, ingredients, meal_type, user_id) VALUES (%s, %s, %s, %s)", 
                   (food_name, ingredients, meal_type, user_id))
    conn.commit()

    print(f"Recipe for {food_name} added successfully!")
    conn.close()
    return True  # Recipe added successfully

# Update a Recipe (including ingredients and meal_type)
def update_recipe(food_name, ingredients, meal_type):
    print("\n=== Update Food Recipe ===")

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM recipes WHERE food_name = %s", (food_name,))
    if not cursor.fetchone():
        print(f"{food_name} does not exist. Use 'Add Food Recipe' to add it.")
        conn.close()
        return False  # Recipe does not exist

    cursor.execute("UPDATE recipes SET ingredients = %s, meal_type = %s WHERE food_name = %s", 
                   (ingredients, meal_type, food_name))
    conn.commit()

    print(f"Recipe for {food_name} updated successfully!")
    conn.close()
    return True  # Recipe updated successfully

# Remove a Recipe
def remove_recipe(food_name):
    print("\n=== Remove Food Recipe ===")

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM recipes WHERE food_name = %s", (food_name,))
    if cursor.fetchone():
        cursor.execute("DELETE FROM recipes WHERE food_name = %s", (food_name,))
        conn.commit()
        print(f"Recipe for {food_name} removed successfully!")
    else:
        print(f"{food_name} does not exist.")

    conn.close()

# Display Food List (including ingredients and meal_type)
def display_food_list():
    print("\n=== Food List ===")

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT food_name, meal_type FROM recipes")
    foods = cursor.fetchall()

    if not foods:
        print("No recipes available.")
    else:
        for index, food in enumerate(foods, start=1):
            print(f"{index}. {food[0]} (Meal Type: {food[1]})")

    conn.close()

# Main Menu (for command line interface)
def main():
    create_tables()  # Create tables if they don't exist

    while True:
        print("\n=== Main Menu ===")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter your choice: ").strip()

        if choice == '1':
            username = input("Enter a username: ").strip()
            password = input("Enter a password: ").strip()
            if register(username, password):
                print("Registration successful!")
        elif choice == '2':
            username = input("Enter your username: ").strip()
            password = input("Enter your password: ").strip()
            user_id = login(username, password)
            if user_id:
                while True:
                    print("\n=== Recipe Menu ===")
                    print("1. Search Food Recipe")
                    print("2. Add Food Recipe")
                    print("3. Update Food Recipe")
                    print("4. Remove Food Recipe")
                    print("5. Display Food List")
                    print("6. Logout")
                    recipe_choice = input("Enter your choice: ").strip()

                    if recipe_choice == '1':
                        food_name = input("Enter the name of the food: ").strip()
                        search_recipe(food_name)
                    elif recipe_choice == '2':
                        food_name = input("Enter the name of the food: ").strip()
                        ingredients = input("Enter the ingredients: ").strip()
                        meal_type = input("Enter the meal type: ").strip()
                        add_recipe(user_id, food_name, ingredients, meal_type)
                    elif recipe_choice == '3':
                        food_name = input("Enter the name of the food to update: ").strip()
                        ingredients = input("Enter the new ingredients: ").strip()
                        meal_type = input("Enter the new meal type: ").strip()
                        update_recipe(food_name, ingredients, meal_type)
                    elif recipe_choice == '4':
                        food_name = input("Enter the name of the food to remove: ").strip()
                        remove_recipe(food_name)
                    elif recipe_choice == '5':
                        display_food_list()
                    elif recipe_choice == '6':
                        print("Logging out...\n")
                        break
                    else:
                        print("Invalid choice. Try again.")
        elif choice == '3':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
