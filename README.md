import tkinter as tk
from tkinter import messagebox, simpledialog, Entry
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
        conn.close()
        return True  # Registration success
    except mysql.connector.errors.IntegrityError:
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
        return result[0]  # Return user ID
    else:
        return None  # Invalid login

# Add a Recipe
def add_recipe(user_id, food_name, ingredients, meal_type):
    conn = connect_db()
    cursor = conn.cursor()

    # Check if the food already exists
    cursor.execute("SELECT * FROM recipes WHERE food_name = %s", (food_name,))
    if cursor.fetchone():
        conn.close()
        return False  # Recipe already exists

    # Insert the recipe with the foreign key (user_id)
    cursor.execute("INSERT INTO recipes (food_name, ingredients, meal_type, user_id) VALUES (%s, %s, %s, %s)", 
                   (food_name, ingredients, meal_type, user_id))
    conn.commit()
    conn.close()
    return True  # Recipe added successfully

# Update a Recipe
def update_recipe(food_name, ingredients, meal_type):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM recipes WHERE food_name = %s", (food_name,))
    if not cursor.fetchone():
        conn.close()
        return False  # Recipe does not exist

    cursor.execute("UPDATE recipes SET ingredients = %s, meal_type = %s WHERE food_name = %s", 
                   (ingredients, meal_type, food_name))
    conn.commit()
    conn.close()
    return True  # Recipe updated successfully

# Remove a Recipe
def remove_recipe(food_name):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM recipes WHERE food_name = %s", (food_name,))
    if cursor.fetchone():
        cursor.execute("DELETE FROM recipes WHERE food_name = %s", (food_name,))
        conn.commit()
    conn.close()

# Display Food List
def display_food_list(user_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT food_name, meal_type FROM recipes WHERE user_id = %s", (user_id,))
    foods = cursor.fetchall()
    conn.close()
    return foods  # Return the list of foods

# Search Recipe
def search_recipe(user_id, food_name):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT food_name, ingredients, meal_type FROM recipes WHERE user_id = %s AND food_name LIKE %s", 
                   (user_id, f"%{food_name}%"))
    results = cursor.fetchall()
    conn.close()
    return results  # Return the list of matching recipes

# GUI Class
class RecipeApp:
    def __init__(self, master):
        self.master = master
        master.title("Recipe Management System")
        master.geometry("400x600")
        master.configure(bg="#f0f0f0")

        self.main_frame = tk.Frame(master, bg="#f0f0f0")
        self.main_frame.pack(pady=20)

        self.username_label = tk.Label(self.main_frame, text="Username:", bg="#f0f0f0")
        self.username_label.pack(pady=5)
        self.username_entry = tk.Entry(self.main_frame)
        self.username_entry.pack(pady=5)

        self.password_label = tk.Label(self.main_frame, text="Password:", bg="#f0f0f0")
        self.password_label.pack(pady=5)
        self.password_entry = tk.Entry(self.main_frame, show="*")
        self.password_entry.pack(pady=5)

        self.login_button = tk.Button(self.main_frame, text="Login", command=self.login, bg="#4CAF50", fg="white")
        self.login_button.pack(pady=10)

        self.register_button = tk.Button(self.main_frame, text="Register", command=self.register, bg="#2196F3", fg="white")
        self.register_button.pack(pady=5)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        user_id = login(username, password)

        if user_id:
            self.open_recipe_manager(user_id)
        else:
            messagebox.showerror("Login Error", "Invalid username or password.")

    def register(self):
        username = simpledialog.askstring("Register", "Enter username:")
        password = simpledialog.askstring("Register", "Enter password:", show='*')

        if username and password:
            if register(username, password):
                messagebox.showinfo("Registration", "Registration successful! You can now log in.")
            else:
                messagebox.showerror("Registration Error", "Username already exists.")
        else:
            messagebox.showwarning("Input Error", "Both username and password are required.")

    def open_recipe_manager(self, user_id):
        self.main_frame.pack_forget()  # Hide the login frame
        self.recipe_window = tk.Frame(self.master, bg="#f0f0f0")
        self.recipe_window.pack(pady=20)

        self.current_user_id = user_id

        # Title Label
        self.recipe_title_label = tk.Label(self.recipe_window, text="Recipe Manager", font=("Arial", 18), bg="#f0f0f0")
        self.recipe_title_label.pack(pady=20)

        # Search Bar
        self.search_entry = Entry(self.recipe_window, width=30)
        self.search_entry.pack(pady=10)
        self.search_button = tk.Button(self.recipe_window, text="Search Recipe", command=self.search_recipe_window, width=20, bg="#FFC107", fg="black")
        self.search_button.pack(pady=5)

        # Buttons Frame
        self.recipe_button_frame = tk.Frame(self.recipe_window, bg="#f0f0f0")
        self.recipe_button_frame.pack(pady=10)

        self.add_recipe_button = tk.Button(self.recipe_button_frame, text="Add Recipe", command=self.add_recipe_window, width=20, bg="#FFC107", fg="black")
        self.add_recipe_button.grid(row=0, column=0, padx=5, pady=5)

        self.update_recipe_button = tk.Button(self.recipe_button_frame, text="Update Recipe", command=self.update_recipe_window, width=20, bg="#FFC107", fg="black")
        self.update_recipe_button.grid(row=0, column=1, padx=5, pady=5)

        self.remove_recipe_button = tk.Button(self.recipe_button_frame, text="Remove Recipe", command=self.remove_recipe_window, width=20, bg="#f44336", fg="white")
        self.remove_recipe_button.grid(row=1, column=0 , padx=5, pady=5)

        self.display_button = tk.Button(self.recipe_button_frame, text="Display Food List", command=self.display_food_list_window, width=20, bg="#2196F3", fg="white")
        self.display_button.grid(row=1, column=1, padx=5, pady=5)

        self.logout_button = tk.Button(self.recipe_window, text="Logout", command=self.logout, width=20, bg="#f44336", fg="white")
        self.logout_button.pack(pady=5)

    def search_recipe_window(self):
        food_name = self.search_entry.get()
        if food_name:
            results = search_recipe(self.current_user_id, food_name)
            if results:
                result_list = "\n".join([f"{index + 1}. {result[0]} (Meal Type: {result[2]})" for index, result in enumerate(results )])
                messagebox.showinfo("Search Results", result_list)
            else:
                messagebox.showinfo("Search Results", "No matching recipes found.")
        else:
            messagebox.showwarning("Input Error", "Please enter a food name to search.")

    def add_recipe_window(self):
        food_name = simpledialog.askstring("Add Recipe", "Enter food name:")
        ingredients = simpledialog.askstring("Add Recipe", "Enter ingredients:")
        meal_type = simpledialog.askstring("Add Recipe", "Enter meal type:")
        
        if food_name and ingredients and meal_type:
            if add_recipe(self.current_user_id, food_name, ingredients, meal_type):
                messagebox.showinfo("Success", "Recipe added successfully!")
            else:
                messagebox.showerror("Error", "Recipe already exists.")
        else:
            messagebox.showwarning("Input Error", "All fields are required.")

    def update_recipe_window(self):
        food_name = simpledialog.askstring("Update Recipe", "Enter food name to update:")
        if food_name:
            ingredients = simpledialog.askstring("Update Recipe", "Enter new ingredients:")
            meal_type = simpledialog.askstring("Update Recipe", "Enter new meal type:")
            
            if ingredients and meal_type:
                if update_recipe(food_name, ingredients, meal_type):
                    messagebox.showinfo("Success", "Recipe updated successfully!")
                else:
                    messagebox.showerror("Error", "Recipe does not exist.")
            else:
                messagebox.showwarning("Input Error", "All fields are required.")
        else:
            messagebox.showwarning("Input Error", "Food name is required.")

    def remove_recipe_window(self):
        food_name = simpledialog.askstring("Remove Recipe", "Enter food name to remove:")
        if food_name:
            remove_recipe(food_name)
            messagebox.showinfo("Success", "Recipe removed successfully!")
        else:
            messagebox.showwarning("Input Error", "Food name is required.")

    def display_food_list_window(self):
        foods = display_food_list(self.current_user_id)
        if foods:
            food_list = "\n".join([f"{food[0]} (Meal Type: {food[1]})" for food in foods])
            messagebox.showinfo("Food List", food_list)
        else:
            messagebox.showinfo("Food List", "No recipes found.")

    def logout(self):
        self.recipe_window.pack_forget()  # Hide the recipe manager frame
        self.main_frame.pack(pady=20)  # Show the login frame
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)

if __name__ == "__main__":
    create_tables()  # Ensure tables are created before running the app
    root = tk.Tk()
    app = RecipeApp(root)
    root.mainloop()
