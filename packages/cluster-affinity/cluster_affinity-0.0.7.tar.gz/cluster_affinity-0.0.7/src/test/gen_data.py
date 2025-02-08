import dendropy
from dendropy.simulate import treesim 
import tqdm
import os

ntax = 1000
schema="nexus"
folder="test_trees"
ntrees = 10

for i in tqdm.tqdm(range(ntrees)):
    t1 = treesim.birth_death_tree(birth_rate=1.0,death_rate=0.5,num_extant_tips=ntax)
    fpath = os.path.join(folder,"{}_{}.tre".format(i,schema))
    t1.write(path=fpath,schema=schema)


l = []
for i in tqdm.tqdm(range(ntrees)):
    t1 = treesim.birth_death_tree(birth_rate=1.0,death_rate=0.5,num_extant_tips=ntax)
    l.append(t1)
lpath = os.path.join(folder,"list_{}.tre".format(schema))
dendropy.TreeList(l).write(path=lpath,schema=schema)

    

for i in tqdm.tqdm(range(10)):
    t1 = treesim.birth_death_tree(birth_rate=1.0,death_rate=0.5,num_extant_tips=ntax)
    t1.deroot()
    fpath = os.path.join(folder,"u{}_{}.tre".format(i,schema))
    t1.write(path=fpath,schema="nexus")

