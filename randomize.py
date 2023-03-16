# source for recipes.json: https://frosch.cosy.sbg.ac.at/datasets/json/recipes
import random 
import json
from rich.console import Console
from storedRecipes import * 

def randomize():
    """ Genreates random number, and opens random_recipes.json file to print and return the recipe at that random number. """

    console = Console()
    # generate random number bw range of recipes
    with Halo(text = "Generating random recipe...", text_color = "cyan", spinner ="hearts"):    
        time.sleep(3.0)

    num = random.randint(1,385)

    # open json file and get recipe dictionary at random number value generated 
    with open("random_recipes.json") as f:
        content = json.loads(f.read())

        recipe = content[num]  
        console.print(":smiley: Random recipe found! \n", style="green1")

        console.print(recipe["Name"], style="orchid1")
        console.print(recipe["url"])
        console.print(recipe["Description"])

        console.print("Ingredients:")
        console.print(recipe["Ingredients"][0])

        console.print("Instructions:")
        console.print(recipe["Method"][0])
        console.print("\n")

        # return recipe dict
            
        time.sleep(1.0)
        return recipe 
