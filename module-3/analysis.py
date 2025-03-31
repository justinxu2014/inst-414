import pandas as pd
import json
import scipy

with open("ingr_map.pkl", "rb") as file:
    ingr_map = pd.read_pickle(file)
    ingr_names = {}

    for idx, row in ingr_map.iterrows():
        if row["id"] not in ingr_names:
            ingr_names[row["id"]] = row["replaced"]

RECIPES = pd.read_csv("PP_recipes.csv", nrows=1000)
RAW_RECIPES = pd.read_csv("RAW_recipes.csv")

rec_names = {}
for idx, row in RAW_RECIPES.iterrows():
        if row["id"] not in rec_names:
            rec_names[row["id"]] = row["name"]

temp = []

for idx in range(len(RECIPES["id"])):
    temp.append([0] * max(ingr_map["id"] + 1))

for idx in range(len(temp)): 
    for ingredient_id in json.loads(RECIPES.iloc[idx]["ingredient_ids"]):
        temp[idx][ingredient_id] = 1

col= list(range(0 , max(ingr_map["id"] + 1)))

DF = pd.DataFrame.from_records(data=temp, columns=col, index=RECIPES["id"])

# Select target for comparison
target = 424415 
target_ = DF.loc[target]

eucDistances = scipy.spatial.distance.cdist(DF,[target_], metric="euclidean").flatten()
euc_query_distances = list(zip(DF.index, eucDistances)) 
eucTopSim = sorted(euc_query_distances, key= lambda x:x[1], reverse=False)[:20]

for x in eucTopSim:
    print('{:<8} {:<50} {:<16}'.format(x[0], rec_names[x[0]], x[1]))
