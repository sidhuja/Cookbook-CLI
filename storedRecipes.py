# table that contains stored recipes 
from banner import * 
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
import pymongo 
from pymongo import MongoClient
import time 
import inquirer  # noqa
from inquirer.themes import GreenPassion
from spinners import Spinners 
from halo import Halo 

cluster = MongoClient("mongodb+srv://test:test@cluster0.atw1fra.mongodb.net/?retryWrites=true&w=majority")
console = Console()
db = cluster["recipes"]
collection = db["recipe"]

def selection_list(action_str, message_str, choices_list):
    """ Takes string action, message, and chocices list as a paramter, displays selection to console and returns string value of desired action"""
    questions = [
        inquirer.List(action_str,
        message=message_str,
        choices=choices_list,)
    ]

    answers = inquirer.prompt(questions, theme = GreenPassion())
    return answers[action_str]

def format_table(table):
    table.row_styles = ["plum1", "pink1", "light_pink1",  "light_salmon1","sandy_brown", "orange1", "orchid1","orchid2","pale_violet_red1", "light_coral" ]
    return table

def view_recipes():
    """ Prints table with data of stored recipes in mongoDB database"""
    # create table with header 
    table = create_table("My Recipes")

    # check if there is data already in mongoDB 
    x = collection.find()
    count = 0
    for data in x:
        count += 1 

    if count == 0:
        console.print("There are no recipes stored yet." , style="bright_red")
        return 
    
    # transfer mongoDB data to table created 
    db = collection.find()
    # add each data in mongodb to table row
    for data_dict in db:
        name = data_dict["name"]
        meal_type = data_dict["meal"]
        ingredients = data_dict["ingredients"]
        instructions = data_dict["instructions"]

        table.add_row(name, meal_type, ingredients, instructions)

    formatted_table = format_table(table)
    console.print(formatted_table)
    time.sleep(2.0)

    # get user to select next desired action
    selected_action = selection_list("actions", "What do you want to do next?",[
                    "Delete a recipe","View based on Meal Type", "Return to Main Menu", "Abort"] )
    
    if selected_action == "Delete a recipe":
        delete_stored_recipes()
    elif selected_action == "View based on Meal Type":
        view_recipe_of_meal_type()
    elif selected_action == "Abort":
        exit_banner() 

def search_database():
    """ Iterates through mongoDB database to find Recipe of given Meal Type string parameter, and prints a table to console of those recipes"""

    # transfer mongoDB data to table created 
    db = collection.find()
    # add each data in mongodb to table row
    for data_dict in db:
        meal_type = data_dict["meal"]

def view_recipe_of_meal_type():
    """ Returns table of stored recipes based off desired Meal Type of Breakfast, Lunch or Dinner. """

    # get string of users desired action 
    selected_action = selection_list("meal", "Select Meal Type",
                                     ["Breakfast","Lunch","Dinner", "Return Back", "Abort"] )
    if selected_action == "Abort":
        exit_banner() 
    elif selected_action == "Return Back":
        return 
    
     # create table with title of selected Meal Type  
    table = create_table("My " + selected_action + " Recipes")

    count = 0
    db = collection.find()
    # add each data in mongodb to table row
    for data_dict in db:
        meal_type = data_dict["meal"]
        # if document has the desired meal type, add recipe to table  
        if meal_type == selected_action:
            count += 1 
            table.add_row(data_dict["name"], meal_type, data_dict["ingredients"], data_dict["instructions"])
    
    # if no recipes found, print error message 
    if count == 0:
        console.print("No recipes found of Meal Type " + selected_action + ". Try again.\n", style="bright_red")
        view_recipe_of_meal_type()

    # if recipe found, print table 
    else:
        formatted_table = format_table(table)
        console.print(formatted_table)
        time.sleep(2.0)


def delete_stored_recipes():
    """ Deletes a stored recipe of a certain index from MongoDB database """

    print("Which row do you want to delete? Enter a number. ", end=" ")
    user_input = int(input())

    # iterate over mongodb collection to find the document to delete 
    number_recipes = 0 
    x = collection.find()
    deleted_recipe = False 

    with Halo(text = "Deleting recipe...", text_color = "cyan", spinner ="hearts"):
        time.sleep(3.0)
        for data_dict in x:
            number_recipes += 1 

            if number_recipes == user_input:
                collection.delete_one(data_dict)
                deleted_recipe = True
                
    # if recipe deleted, display the successfully deleted message         
    if deleted_recipe == True:
        console.print("\nSucessfully deleted recipe\n", style="green1")
        
    # if user inputs number greater than total documents in database, or a negative number, print error message
    if user_input > number_recipes or user_input <= 0 :
        # display the error message 
        print("Error. You entered a row that is out of bounds. Try again")
        delete_stored_recipes()


def create_table(table_title):
    """ Creates table with columns which will store recipes, and returns the table"""
    table = Table(title = table_title, show_header=True, header_style= "bold bright_white", show_lines=True)
    table.add_column("Name")
    table.add_column("Meal Type")
    table.add_column("Ingredients")
    table.add_column("Instructions")
    return table 

def store_recipe(name, meal_type, ingredients, instructions):
    """ Helper function for get_user_function() and takes Recipe's string name, description, ingredients, and instructoins as paramters
    and stores that in mongoDB database. """

    recipe = {
        "name": name,
        "meal": meal_type,
        "ingredients" : ingredients,
        "instructions" : instructions
    }

    # insert data 
    collection.insert_one(recipe)

    console.print("Sucessfully stored recipe for " + name + "\n", style="green1")

def add_generated_recipe(recipe_text):
    """Takes string text from recipe file as a paramter, and stores in database"""

    recipe_lines = recipe_text.split("\n")
            
    count = 0 
    ingredients_string = ""
    instructions_string = ""
    ingredients_line = False 
    instructions_line = False 

    # iterate through lines in text to find recipe data name, instructions, and ingredients 
    for line in recipe_lines:
        count += 1 
        # if iteration is on the first line of text, get name of recipe
        if count == 1:
            name = line 
        
        if line == "Ingredients:":
            ingredients_line = True 
            continue 

        if line == "Instructions:":
            instructions_line = True 
            continue 

        # if the Ingredients text has been reached, add text to ingredients list 
        if ingredients_line is True and line.strip() != '' : 
            ingredients_string += line 

        # if end of Ingredients text is reached, continue to next line
        if ingredients_line is True and line.strip() == '': 
            ingredients_line = False 
            continue

        # if Instructions text is reached, add text to instructions list 
        if instructions_line is True and line.strip() != '' : 
            instructions_string += line

    # add data to mongoDB 
    store_recipe(name, " ", ingredients_string, instructions_string)
        

def get_user_input():
    """ Gets name, descriptoion, ingredients, and instructions of recipe from user and calls store_recipe() 
    with those paramters"""
    inputted_name = Prompt.ask("Enter recipe name")
    inputted_meal = Prompt.ask("Enter Breakfast, Lunch OR Dinner)")
    inputted_ingredients = Prompt.ask("Enter recipe ingredients")
    inputted_instructions = Prompt.ask("Enter recipe instructions")
    print("\n")
    # store inputed recipe in database
    store_recipe(inputted_name, inputted_meal, inputted_ingredients, inputted_instructions)

