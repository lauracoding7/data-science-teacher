# pylint: disable=missing-docstring,line-too-long
import sys
from os import path
import csv
from bs4 import BeautifulSoup
import requests

PAGES_TO_SCRAPE = 3

def parse(html):
    ''' return a list of dict {name, difficulty, prep_time} '''
    # YOUR CODE HERE
    # html -> <_io.TextIOWrapper name='pages/carrot.html' mode='r' encoding='UTF-8'>
    recipe_list = []
    soup = BeautifulSoup(html, "html.parser")
    for recipe in soup.find_all('div', class_= 'p-2 recipe-details'):
        recipe_list.append(parse_recipe(recipe))
    return recipe_list

def parse_recipe(article):
    ''' return a dict {name, difficulty, prep_time} modelising a recipe'''
    # YOUR CODE HERE
    recipe_name = article.find("p", class_="text-dark text-truncate w-100 font-weight-bold mb-0 recipe-name").text
    recipe_difficulty = article.find("span", class_="recipe-difficulty").text
    recipe_prep_time = article.find("span", class_="recipe-cooktime").text
    return {"name": recipe_name , "difficulty": recipe_difficulty, "prep_time": recipe_prep_time}

def write_csv(ingredient, recipes):
    ''' dump recipes to a CSV file `recipes/INGREDIENT.csv` '''
    # YOUR CODE HERE
    with open(f'recipes/{ingredient}.csv', 'w') as recipe_file:
        keys = recipes[0].keys()
        writer = csv.DictWriter(recipe_file, fieldnames=keys)
        writer.writeheader()
        writer.writerows(recipes)

def scrape_from_internet(ingredient, start=1):
    ''' Use `requests` to get the HTML page of search results for given ingredients. '''
    # YOUR CODE HERE
    url = "https://recipes.lewagon.com/?search"
    params = {"page": start, "search[query]": ingredient}
    response = requests.get(url, params=params)
    if response.history:
        return None
    return response.text

def scrape_from_file(ingredient):
    file = f"pages/{ingredient}.html"
    if path.exists(file):
        return open(file)
    print("Please, run the following command first:")
    print(f'curl -g "https://recipes.lewagon.com/?search[query]={ingredient}" > pages/{ingredient}.html')
    sys.exit(1)


def main():
    if len(sys.argv) > 1:
        ingredient = sys.argv[1]
        # Replace scrape_from_file with scrape_from_internet and implement pagination (more than 2 pages needed)
        recipes = parse(scrape_from_internet(ingredient))

        # YOUR CODE HERE
        recipes = []
        for page in range(PAGES_TO_SCRAPE):
            response = scrape_from_internet(ingredient, page+1)
            if response:
                recipes += parse(response)
            else:
                break

        write_csv(ingredient, recipes)
    else:
        print('Usage: python recipe.py INGREDIENT')
        sys.exit(0)


if __name__ == '__main__':
    main()
