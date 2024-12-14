# Recipe Management System Overview
The Recipe Management System is a Python-based application that allows users to efficiently manage their food recipes. Integrated with a MySQL database, the system provides features for user registration, login, and recipe management.

 # Features:
User Registration & Login: Secure user accounts allow for personalized recipe management.
Recipe Management: Users can add new recipes, modify existing ones, search for recipes by name, and delete recipes.
Personalized Access: Recipes are linked to individual users, ensuring tailored access and modifications.
User Interface: The system offers a simple, menu-based interface for ease of navigation, with options to access and manage recipes.
Data Handling: The use of Python for backend functionality and MySQL for database management ensures efficient and secure data processing.
This system is designed for anyone looking to organize and store recipes in a secure, organized, and user-friendly way.

 # Python Concepts and Libraries
Tkinter:
Purpose: Tkinter is used for creating the graphical user interface (GUI) of the application.
# Key Features:
GUI Components: It provides windows, buttons, dialogs, and other interactive elements for the application.
Main Window: Includes a login and registration interface, and recipe management windows after user login.
Widgets:
Button Widget: Used for tasks like registration, login, and managing recipes.
simpledialog: Prompts users for input (e.g., food names, ingredients, meal types).
messagebox: Displays success or error notifications to communicate with the user.
 
 # MySQL Database Integration
The MySQL database serves as the backend for managing user and recipe data within the system.

# Key Features:
Database Connection: The system uses the mysql.connector library to connect to the MySQL database running on localhost.
Connection Handling: The connect_db() function is responsible for establishing the database connection, and queries are executed using cursor.execute().
 # Data Integrity:
The system automatically creates necessary tables (users and recipes) if they don't exist using SQL CREATE TABLE commands.
Foreign Key: The user_id in the recipes table links each recipe to a specific user for personalized access and management.
# User Authentication:
Registration: The register() function uses SQL INSERT INTO to add new users.
Login: The login() function uses SQL SELECT to verify user credentials.
Error Handling: Integrity errors, such as inserting duplicate usernames, are intercepted to ensure smooth operation and user-friendly error messages.
 # Recipe Management:
CRUD Operations: SQL commands such as INSERT, UPDATE, SELECT, and DELETE are used for adding, modifying, searching, and deleting recipes.
Error Prevention: If a recipe is not found during a search or update, the system provides a polite notification rather than allowing crashes or unhandled exceptions.

 # Sustainable Development Goals (SDGs)
# SDG 3: Good Health and Well-being
Healthy Living: The system helps users access and organize recipes that promote balanced nutrition, supporting healthier living.
Recipe Search: Users can search for recipes based on ingredients and meal types, allowing them to make health-conscious choices.
Dietary Needs: It aids users in planning meals that fit their specific dietary requirements, encouraging better nutrition and overall health.
# SDG 12: Responsible Consumption and Production
Minimizing Food Waste: By allowing users to plan meals based on available ingredients, the system helps reduce food waste.
Efficient Resource Management: It helps users avoid purchasing unnecessary ingredients by maintaining a well-organized recipe collection, promoting responsible consumption and production.

# SDG 17: Partnerships for the Goals
Community Building: Users can exchange recipes, expertise, and advice on health-conscious cooking, forming a supportive network focused on health and sustainability.
Potential Collaborations: The system could expand by collaborating with health experts, nutritionists, and local food suppliers to enhance the user experience, provide professional advice, and promote healthier, more sustainable lifestyle habits.
 
 # Program/System Instructions
# Registering a User:
Click the "Register" button on the main window.
Enter a unique username and password when prompted.
If the username is unique, registration will succeed. Otherwise, an error message will be shown.
# Logging in:
Click the "Login" button on the main window.
Enter your username and password.
If credentials match, you will be logged in and redirected to the recipe management window. If the credentials are invalid, an error message will appear.
Managing Recipes (Available after login):
# Searching for a Recipe:

Enter the food name in the search bar to find a recipe.
# Adding a Recipe:

Click the "Add Recipe" button.
Enter the food name, ingredients, and meal type to add a new recipe.
# Updating a Recipe:

Click the "Update Recipe" button.
Enter the food name you wish to update, and provide the new ingredients and meal type.
# Removing a Recipe:

Click the "Remove Recipe" button.
Enter the food name of the recipe you want to delete.
# Displaying Recipe List:

Click the "Display Food List" button to view all your added recipes, including their meal type.
# Logging Out:
Click the "Logout" button in the recipe management window to log out and close the recipe manager.
