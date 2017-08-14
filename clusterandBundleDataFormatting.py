import pandas
import json
import numpy.random as rnd

df = pandas.DataFrame.from_csv('dataSet.csv', 0)

primary = df.loc['Primary Game Type ', :]
secondary = df.loc['Secondary Game Type ', :]

#define nodesDict, for all the nodes included in the plot
nodesDict = {'name':'', 'children':[]}

#dict for calculating games count, only for assisting calculation, is not exported for use in data visualization 
categoryDict = {}

#adding game names
for i in df.columns.values[1:]:
    nodesDict['children'].append({'name': i, 'category':'game', 'GPS': rnd.randint(60, 100)})

#adding secondary type first and primary type at the end so that the primary type end up at the very top
(r, c) = secondary.shape    
for i in range(r):
    if secondary.iloc[i, 0][0] == ' ':
        if(secondary.iloc[i, 0] == ' Casino'):
            nodesDict['children'].append({'name': secondary.iloc[i, 0], 'category': 'secondary'})
            categoryDict[secondary.iloc[i, 0]] = 0
        else:
            nodesDict['children'].append({'name': secondary.iloc[i, 0][1:], 'category': 'secondary'})
            categoryDict[secondary.iloc[i, 0][1:]] = 0
    else:
        nodesDict['children'].append({'name': secondary.iloc[i, 0], 'category': 'secondary'})
        categoryDict[secondary.iloc[i, 0]] = 0
    
#primary game type values:
(r, c) = primary.shape
for i in range(r):
    if primary.iloc[i, 0][0] == ' ':
        nodesDict['children'].append({'name': primary.iloc[i, 0][1:], 'category': 'primary'})  #add category name to nodesDict
        categoryDict[primary.iloc[i, 0][1:]] = 0 #initialize categoryDict
    else:
        nodesDict['children'].append({'name': primary.iloc[i, 0], 'category': 'primary'})
        categoryDict[primary.iloc[i, 0]] = 0

#file output
with open('relations.json', 'w') as outfile:
    json.dump(relations, outfile)
        
#counting how many games fall into each category
for i in range(len(relations)):
    categoryDict[relations[i]['target']] += 1

#adding the calculated sum to the JSON nodesDict
for i in categoryDict:
    for j in nodesDict['children']:
        if j['name'] == i:
            j['gamesCount'] = categoryDict[i]

#file output
with open('nodes.json', 'w') as outfile:
    json.dump(nodesDict, outfile)