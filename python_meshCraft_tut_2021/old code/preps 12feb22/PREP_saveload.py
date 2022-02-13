"""Save and load"""

# ***
def load_world(terrain,subject):
    import pickle, sys, os, copy
    from ursina import destroy

    # Open main module directory for correct file.
    path = os.path.dirname(os.path.abspath(sys.argv[0]))
    os.chdir(path)
    with open('test_map2.mm', 'rb') as f:
        nd = pickle.load(f)

        # Empty out current terrain.
        for s in terrain.subsets:
            destroy(s)
        terrain.td={}
        terrain.vd={}
        terrain.subsets=[]
        terrain.setup_subsets()
        terrain.currentSubset=1
        terrain.td=copy.copy(nd[1])
        # Iterate over terrain dictionary and
        # if we find 't' then generate a block.
        # Note this means we'll lose colour info etc.
        i = 0
        for key in terrain.td:
            if terrain.td.get(key)=='t':
                x = key[0]
                y = key[1]
                z = key[2]
                if i>=len(terrain.subsets)-1:
                    i=0
                terrain.genBlock(x,y,z,subset=i,gap=False,blockType='grass')
                i+=1

        # Reset swirl engine.
        terrain.swirlEngine.reset(  subject.position.x,
                                    subject.position.z)
        for s in terrain.subsets:
            s.model.generate()
        # And reposition subject according to saved map.
        subject.position=copy.copy(nd[0])

def save_world(terrain,subject):
    import pickle, sys, os

    # Open main module directory for correct file.
    path = os.path.dirname(os.path.abspath(sys.argv[0]))
    os.chdir(path)
    with open('test_map2.mm', 'wb') as f:
        
        new_data=[subject.position,terrain.td]

        pickle.dump(new_data, f)
        new_data.clear()