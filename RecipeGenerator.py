'''
A program that generates recipes for user
source for recipes.json: https://frosch.cosy.sbg.ac.at/datasets/json/recipes
'''

from random import choice
import random
import time
import json

if __name__ == '__main__':
    while True:
        time.sleep(1.0)

        # read line in recipe file
        f = open("recipes.txt", "r")
        line = f.readline()
        f.close()

        if line.isalpha():
            # load json file
            with open("recipes.json") as f:
                content = json.loads(f.read())

            # finds recipes with ingredient indicated
            contains_ingredients = {'Contains Ingredients': []}
            random_number = random.randint(0, 800)
            i = random_number
            for item in content[i]['Ingredients']:
                if line not in item:
                    continue
                else:
                    print("found")
                    f = open("recipes.txt", "w")
                    f.write(content[i]['Name'] + "\n" + "\n")
                    f.write("Ingredients:" + "\n")
                    for ingredient in content[i]['Ingredients']:
                        f.write(ingredient + "\n")
                    f.write("\n" + "Instructions:" + "\n")
                    for step in content[i]['Method']:
                        f.write(step + "\n")
                # if not found keep going to different index
                i = i + 1