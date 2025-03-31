import pandas as pd
import json
import networkx as nx

with open("ingr_map.pkl", "rb") as file:
    ingr_map = pd.read_pickle(file)
    ingr_names = {}

    for idx, row in ingr_map.iterrows():
        if row["id"] not in ingr_names:
            ingr_names[row["id"]] = row["replaced"]

RECIPES = pd.read_csv("PP_recipes.csv", nrows=1000)

g = nx.Graph()

uniq = ingr_map.drop_duplicates(subset=["id"])
for idx, row in uniq.iterrows():
    g.add_node(row["id"], name= row["replaced"])

for idx , row in RECIPES.iterrows():
    i= 0
    for left_ingr in json.loads(row["ingredient_ids"]):
        for right_ingr in json.loads(row["ingredient_ids"])[i+1:]:
          g.add_edge(left_ingr, right_ingr)
        i += 1
highest = sorted(g.degree, key = lambda x : x[1], reverse= True)
print("Top 20 most used ingredients ")
{print('{:<4}{:<8}{:<6}{:<30}{:<11}{:<4}'.format("ID: ", degree[0], "Name: ", g.nodes[degree[1]]["name"], "neighbors: ", degree[1])) for degree in highest[:20]}
