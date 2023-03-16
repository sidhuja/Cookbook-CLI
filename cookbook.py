from banner import * 
from storedRecipes import * 
from randomize import * 
from rich.console import Console
from rich import print 
import os
import sys
from pprint import pprint
sys.path.append(os.path.realpath("."))
import inquirer  # noqa
from inquirer.themes import GreenPassion
import time 


def selection_list(action_str, message_str, choices_list):
    """ Takes string action, message, and chocices list as a paramter, displays selection to console and returns string value of desired action"""
    questions = [
        inquirer.List(action_str,
        message=message_str,
        choices=choices_list,)
    ]

    answers = inquirer.prompt(questions, theme = GreenPassion())
    return answers[action_str]

def main_menu():
    """Displays list of Main Menu actions to users, and returns string value of action they want. """
    selected_action = selection_list("actions", "Welcome to the Main Menu", 
                                        ["Store a recipe","View all stored recipes","Get a new recipe", "Abort"])
    return selected_action


def search_ingredient():
    """ Prints recipe based off of string value Ingredient input by communciating with RecipeGenerator microservice via text files """
    console = Console()

    console.print("Type ingredient you want included?", style="orchid1")

    user_input = input()
    # if user inputs ingredient
    if user_input.isalpha():
        # write word to recipes.txt
        f = open("recipes.txt", "w")
        f.write(user_input)
        f.close()

        with Halo(text = "Searching database for recipe...", text_color = "cyan", spinner ="hearts"):    
            time.sleep(5.0)

            # read recipe from text file
            f = open("recipes.txt", "r")
            recipe = f.read()
            recipe_lines = recipe.split("\n")
            
            # check if second line is empty, that means no recipe found 
            count = 0 
            for line in recipe_lines:
                if line:
                    count += 1 

        if count < 3:
            console.print("Ingredient not found in database. \n", style="bright_red")

            # get user to select next desired action
            selected_action = selection_list("actions", "What do you want to do next?",[
                    "Search for another ingredient", "Choose other method to generate recipe ","Return to Main Menu", "Abort"] )

        # if recipes file not empty, search was a success
        else:
            console.print(":smiley: Recipe found!", style="green1")
            time.sleep(2.0)
            print(recipe)
            time.sleep(2.0)
                
            # get user to select next desired actions 
            selected_action = selection_list("actions","What do you want to do next?",
                                                    ["Add recipe to Cookbook ", "Search for another ingredient","Choose other method to generate recipe ","Return to Main Menu", "Abort"] )

        # if user wants to search for another ingredient, start from top again
        if selected_action == "Search for another ingredient":
            search_ingredient() 
        elif selected_action == "Add recipe to Cookbook ":
            add_generated_recipe(recipe)  
        # if user want to choose another method, or return to main menu, return to Choose Method Screen
        elif selected_action == "Choose other method to generate recipe ":
            search_recipe_action() 
        elif selected_action == "Abort":
            exit_banner()

def random_recipe_selection():
    """Gets random recipe and promts user to either add to cookbook, generate another random recipe, choose other generation method, return to main menu, 
    or Abort. """
    # get random recipe dictionary value 
    recipe = randomize()
    
    # ask user if they want to store recipe in database 
    selected_action = selection_list("actions","What do you want to do next? ",
                                        ["Add recipe to Cookbook ", "Generate another random recipe","Choose other method to generate recipe ", "Return to Main Menu", "Abort"])

    # if user wants to search for another ingredient, start from top again
    if selected_action == "Generate another random recipe":
        random_recipe_selection() 

    elif selected_action == "Add recipe to Cookbook ":
        store_recipe(recipe["Name"], " ", recipe["Ingredients"][0], recipe["Method"][0])  

    # if user want to choose another method, or return to main menu, return to Choose Method Screen
    elif selected_action == "Choose other method to generate recipe ":
        search_recipe_action() 
        
    elif selected_action == "Abort":
        exit_banner()
    
def search_recipe_action():
    """ Displays list of Methods to Generate Recipe, and deploys appropraite helper functions based of user selection"""
    
    # get user to select desired action 
    selected_action = selection_list("actions","Choose method to generate recipe",
                                        ["Search an Ingredient","Generate random recipe", "Return to Main Menu", "Abort"])

    if selected_action == "Search an Ingredient":
        search_ingredient()
    elif selected_action == "Return to Main Menu":
        return 
    elif selected_action == "Generate random recipe":
        random_recipe_selection()
    elif selected_action == "Abort":
        exit_banner() 
       
def main():
    # display banner and instructions 
    project_banner()
    project_overview()
    project_instructions()

    while True:
        # get user input on perfered action
        action = main_menu()

        if action == "View all stored recipes":
            view_recipes()
        elif action == "Get a new recipe":
            search_recipe_action()
        elif action == "Store a recipe":
            get_user_input()
        elif action == "Abort":
            exit_banner()
         
        time.sleep(1.0)

if __name__ == "__main__":
    main()