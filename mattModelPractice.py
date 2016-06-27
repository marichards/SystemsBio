from cobra.io.sbml import create_cobra_model_from_sbml_file
from cobra import Model, Reaction, flux_analysis
from copy import deepcopy
import re
import time

start_time = time.time()
# Import Matt's model from SMBL format and creates a model object in cobra
mattModel = create_cobra_model_from_sbml_file("2016_06_23_gapped_meoh_producing.xml")
## Creates a model of universal reactions and reads through the database
# of reactions getting the reaction ID and overall reaction and adding them to
# the universal reactions model
Universal = Model("Universal Reactions")
f = open('2015_test_db.txt', 'r')
# These two functions are used to make our list of functions unique so that no duplicate
# functions are run through the optimization protocol
def uniq(lst):
    last = object()
    for item in lst:
        if item == last:
            continue
        yield item
        last = item
def sort_and_deduplicate(l):
    return list(uniq(sorted(l, reverse=True)))
# Reads through the text file and takes out different data fields (id, reaction)
# that are tab delimited adds them to an dictionary from which they can be added to the
# universal reactions model
rxn_dict = {}
for line in f:
    rxn_items = line.split('\t')
    rxn_dict[rxn_items[0]] = rxn_items[2]
for rxnName in rxn_dict.keys():
    rxn = Reaction(rxnName)
    Universal.add_reaction(rxn)
    rxn.reaction = rxn_dict[rxnName]
# Creates an array to add the value of the objective function after it is optimized
# so that we can compare the various gapfilling solutions
growthValue = []
its = 4
# Runs growMatch gapfilling algorithm on the toyModel taking reactions from universal
result = flux_analysis.growMatch(mattModel, Universal, iterations=1)
resultShortened = sort_and_deduplicate(uniq(result))
rxns_added = {len(resultShortened)}
for i in range(len(resultShortened)):
    [rxns_added[i]] = resultShortened[i]
print rxns_added
# Runs the various solutions given by the gapfilling result through the model and obtains the
# value of the objective function that is garnered by adding these reactions to the model
for x in range(len(resultShortened)):
    mattModelTest = deepcopy(mattModel)
    for i in range(len(resultShortened[x])):
        addID = resultShortened[x][i].id
        rxn = Reaction(addID)
        mattModelTest.add_reaction(rxn)
        rxn.reaction = resultShortened[x][i].reaction
        rxn.reaction = re.sub('\+ dummy\S+', '', rxn.reaction)
    growthValue.append(mattModelTest.optimize().f)
    mattModelTest = mattModel
for i in range(len(growthValue)):
    print growthValue[i]

print "Run time: %s seconds" %(time.time() - start_time)