import cobra.test
import cobra
import pandas

# pandas.options.display.max_rows = 3000
#
#
f = open('modelPractice.txt','w')
cobra_ecolimodel = cobra.test.create_test_model("ecoli")

# for x in cobra_ecolimodel.metabolites:
#     f.write(("%s : %s" %(x.id, x.formula)))
#     f.write('\n')
#
# for x in cobra_ecolimodel.reactions:
#     f.write("%s : %s" %(x.id, x.reaction))
#     f.write('\n')
#
# for x in cobra_ecolimodel.genes:
#     associated_ids = (i.id for i in x.reactions)
#     f.write("%s is associated with reactions %s"
#         %(x.id, "{" + ", ".join(associated_ids) + "}"))
#     f.write('\n')

cobra_ecolimodel.optimize()
print(cobra_ecolimodel.solution.status)
checkVar = round(cobra_ecolimodel.solution.f, 3)
# print checkVar

cobra_ecolimodel.summary()


# fva_output = cobra.flux_analysis.flux_variability_analysis(cobra_ecolimodel)
# f.write(str(pandas.DataFrame.from_dict(fva_output).T.round(5)))

gr, s = cobra.flux_analysis.single_gene_deletion(cobra_ecolimodel)


gr, s = cobra.flux_analysis.single_reaction_deletion(cobra_ecolimodel)
f.write(str(pandas.DataFrame.from_dict({"growth_rate" : gr,"status" : s})))



